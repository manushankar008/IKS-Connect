import json
import re
import time
from collections import defaultdict
from pathlib import Path

import requests

# ============================================================
# SETTINGS
# ============================================================

CHUNK_FILE = Path("data/chunks/kerala/kerala_chunks.txt")
OUTPUT_DIR = Path("knowledge_graph/reports")
MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Keep this small for the first reliable run. Increase after reviewing results.
NUMBER_OF_CHUNKS = 10
REQUEST_TIMEOUT_SECONDS = 240
MAX_RETRIES = 1

# Use only the dedicated Art and Culture document for this extraction pass.
ALLOWED_SOURCE = "art and culture.txt"
ALLOWED_CATEGORY = "culture"

# ============================================================
# SCHEMA
# ============================================================

ALLOWED_TYPES = {
    "State",
    "District",
    "HeritageSite",
    "ArtForm",
    "Festival",
    "TraditionalKnowledge",
    "Person",
    "LiteraryWork",
    "Organization",
}

ALLOWED_RELATIONSHIPS = {
    "PART_OF",
    "LOCATED_IN",
    "PRACTICED_IN",
    "HELD_IN",
    "ASSOCIATED_WITH",
    "CREATED",
}

# Basic endpoint rules. These are conservative checks, not a proof that
# a relationship is factually true.
RELATIONSHIP_RULES = {
    "PART_OF": {
        ("District", "State"),
        ("HeritageSite", "District"),
        ("HeritageSite", "State"),
        ("Organization", "Organization"),
        ("Organization", "State"),
        ("ArtForm", "State"),
        ("Festival", "State"),
        ("TraditionalKnowledge", "State"),
        ("LiteraryWork", "Person"),
        ("LiteraryWork", "Organization"),
    },
    "LOCATED_IN": {
        ("HeritageSite", "District"),
        ("HeritageSite", "State"),
        ("Organization", "District"),
        ("Organization", "State"),
        ("Festival", "District"),
        ("Festival", "State"),
    },
    "PRACTICED_IN": {
        ("ArtForm", "District"),
        ("ArtForm", "State"),
        ("TraditionalKnowledge", "District"),
        ("TraditionalKnowledge", "State"),
    },
    "HELD_IN": {
        ("Festival", "District"),
        ("Festival", "State"),
    },
    "ASSOCIATED_WITH": {
        ("HeritageSite", "ArtForm"),
        ("ArtForm", "HeritageSite"),
        ("ArtForm", "Festival"),
        ("Festival", "ArtForm"),
        ("Organization", "ArtForm"),
        ("ArtForm", "Organization"),
        ("Organization", "HeritageSite"),
        ("HeritageSite", "Organization"),
        ("TraditionalKnowledge", "ArtForm"),
        ("ArtForm", "TraditionalKnowledge"),
        ("HeritageSite", "Festival"),
        ("Festival", "HeritageSite"),
    },
    "CREATED": {
        ("Person", "LiteraryWork"),
    ("Person", "ArtForm"),
        ("Organization", "LiteraryWork"),
    },
}

# A keyword match is only a candidate-selection heuristic. The LLM must
# still extract facts from the actual passage.
CULTURE_KEYWORDS = (
    "theyyam", "kathakali", "kalaripayattu", "mohiniyattam",
    "kerala kalamandalam", "kutiyattam", "kuttampalam",
    "folk art", "traditional art", "cultural heritage", "temple mural",
    "traditional craft", "folk tradition", "ritual art",
    "classical dance", "performing arts", "traditional music",
    "heritage monument", "heritage site", "literature", "handicraft",
    "folklore", "fine arts", "film festival", "museum", "monument",
    "theatre", "theater", "archaeology", "archives",
)

# ============================================================
# HELPERS
# ============================================================

def get_metadata(chunk, field):
    match = re.search(
        rf"^{re.escape(field)}:\s*(.+)$",
        chunk,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    return match.group(1).strip() if match else "Unknown"


def get_chunk_id(chunk):
    match = re.search(r"---\s*CHUNK\s*(\d+)", chunk, re.IGNORECASE)
    return match.group(1) if match else "unknown"


def normalize_name(name):
    return re.sub(r"\s+", " ", name.strip()).casefold()


def parse_json_response(answer):
    """Parse JSON, including a response accidentally wrapped in code fences."""
    answer = answer.strip()
    answer = re.sub(r"^```(?:json)?\s*", "", answer, flags=re.IGNORECASE)
    answer = re.sub(r"\s*```$", "", answer)
    return json.loads(answer)


def select_chunks(all_chunks):
    selected = []
    seen = set()

    for raw_chunk in all_chunks:
        chunk = raw_chunk.strip()
        if not chunk:
            continue

        source = get_metadata(chunk, "SOURCE").casefold()
        category = get_metadata(chunk, "CATEGORY").casefold()
        text_match = re.search(
            r"^TEXT:\s*(.*)$", chunk,
            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )
        body = text_match.group(1).strip() if text_match else chunk

        if source != ALLOWED_SOURCE or category != ALLOWED_CATEGORY:
            continue

        # Do not select title/foreword pages unless they contain a relevant term.
        body_lower = body.casefold()
        if not any(keyword in body_lower for keyword in CULTURE_KEYWORDS):
            continue

        # Avoid duplicate chunks with identical body text.
        body_key = re.sub(r"\s+", " ", body_lower)
        if body_key in seen:
            continue
        seen.add(body_key)

        selected.append(chunk)
        if len(selected) >= NUMBER_OF_CHUNKS:
            break

    return selected


def build_prompt(source, page, body):
    schema = {
        "entities": [
            {
                "name": "exact name copied from passage",
                "type": "one allowed entity type",
                "evidence": "short exact quote supporting the entity",
            }
        ],
        "relationships": [
            {
                "source": "exact entity name",
                "relationship": "one allowed relationship",
                "target": "exact entity name",
                "evidence": "short exact quote supporting this exact relationship",
            }
        ],
    }

    return f"""
You are extracting candidate facts for a Kerala cultural-heritage knowledge graph.

Use only facts explicitly supported by the passage below. Do not use outside knowledge.
Do not guess. Do not infer a relationship just because two names occur in the same passage.
Do not create relationships to the document title or subject heading.
Do not create self-relationships.
Do not turn recommendations or proposals into claims that something already exists.
If the passage does not support a useful fact, return empty arrays.

Entity types and meanings:
- State: a state, such as Kerala.
- District: a district in Kerala.
- HeritageSite: a specific existing heritage building, monument, cultural site, or venue.
- ArtForm: a specific art, performance, craft, music, dance, theatre, or folklore form.
- Festival: a named festival or film festival.
- TraditionalKnowledge: a named traditional practice or body of knowledge.
- Person: a human individual only, never a department, company, board, or institution.
- LiteraryWork: a named book, poem, play, or other literary work.
- Organization: a department, board, corporation, academy, museum organization, or institution.

Allowed relationship types:
- PART_OF: source is a genuine component/member of target.
- LOCATED_IN: source is physically located in target.
- PRACTICED_IN: an art form or traditional knowledge is practiced in a place.
- HELD_IN: a festival/event takes place in a place.
- ASSOCIATED_WITH: use only when the passage explicitly states a meaningful association.
- CREATED: a person or organization created a work, and the passage explicitly says so.

Allowed entity types: {", ".join(sorted(ALLOWED_TYPES))}
Allowed relationship types: {", ".join(sorted(ALLOWED_RELATIONSHIPS))}

Relationship direction matters. For example, a district may be PART_OF a state.
A state is not PART_OF a department. A department is not a person.
Do not make up a District from an unfamiliar word.
Only use entity names that occur literally in the passage.
For every entity and relationship, provide a short exact evidence quote copied from the passage.
Every relationship endpoint must be one of the returned entities.
Return valid JSON only, with this exact structure:
{json.dumps(schema, ensure_ascii=False)}

Source: {source}
Page: {page}

PASSAGE:
{body}
""".strip()


def call_ollama(prompt):
    last_error = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": 0},
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            payload = response.json()
            answer = payload.get("response", "")
            if not answer:
                raise ValueError("Ollama returned an empty response.")
            return answer
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                ValueError) as error:
            last_error = str(error)
            if attempt < MAX_RETRIES:
                time.sleep(2)

    raise RuntimeError(last_error or "Unknown Ollama error")


def exact_quote_is_supported(quote, body):
    if not isinstance(quote, str) or not quote.strip():
        return False
    # Normalized comparison tolerates line breaks inserted during PDF extraction.
    normalize = lambda value: re.sub(r"\s+", " ", value).casefold().strip()
    return normalize(quote) in normalize(body)


def entity_name_occurs(name, body):
    if not isinstance(name, str) or not name.strip():
        return False
    return normalize_name(name) in normalize_name(body)


# ============================================================
# MAIN EXTRACTION
# ============================================================

def main():
    print("Reading chunks...")

    if not CHUNK_FILE.exists():
        print(f"Chunk file not found: {CHUNK_FILE}")
        raise SystemExit(1)

    text = CHUNK_FILE.read_text(encoding="utf-8")
    all_chunks = re.split(r"(?=---\s*CHUNK\s*\d+)", text, flags=re.IGNORECASE)
    selected_chunks = select_chunks(all_chunks)

    if not selected_chunks:
        print("No matching culture chunks found.")
        raise SystemExit(0)

    print(f"Selected {len(selected_chunks)} chunks from {ALLOWED_SOURCE}.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    candidate_entities = {}
    candidate_relationships = {}
    chunk_results = []
    failures = []

    for index, chunk in enumerate(selected_chunks, start=1):
        chunk_id = get_chunk_id(chunk)
        source = get_metadata(chunk, "SOURCE")
        page = get_metadata(chunk, "PAGE")
        text_match = re.search(
            r"^TEXT:\s*(.*)$", chunk,
            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )
        body = text_match.group(1).strip() if text_match else chunk

        print(f"[{index}/{len(selected_chunks)}] Chunk {chunk_id}, page {page}")

        result_for_chunk = {
            "chunk_id": chunk_id,
            "source": source,
            "page": page,
            "entities": [],
            "relationships": [],
            "rejected": [],
            "status": "ok",
        }

        try:
            answer = call_ollama(build_prompt(source, page, body))
            data = parse_json_response(answer)
            if not isinstance(data, dict):
                raise ValueError("Top-level response is not a JSON object.")
        except Exception as error:
            message = str(error)
            print(f"  ERROR: {message}")
            result_for_chunk["status"] = "failed"
            result_for_chunk["error"] = message
            failures.append({
                "chunk_id": chunk_id,
                "source": source,
                "page": page,
                "error": message,
            })
            chunk_results.append(result_for_chunk)
            continue

        chunk_entities = {}
        raw_entities = data.get("entities", [])
        if not isinstance(raw_entities, list):
            raw_entities = []

        for item in raw_entities:
            if not isinstance(item, dict):
                continue

            name = item.get("name")
            entity_type = item.get("type")
            evidence = item.get("evidence", "")

            if not isinstance(name, str) or not isinstance(entity_type, str):
                continue

            name = re.sub(r"\s+", " ", name.strip())
            entity_type = entity_type.strip()

            if not name or entity_type not in ALLOWED_TYPES:
                result_for_chunk["rejected"].append({
                    "kind": "entity",
                    "name": name,
                    "reason": "empty name or disallowed type",
                })
                continue

            if not entity_name_occurs(name, body):
                result_for_chunk["rejected"].append({
                "kind": "entity",
                "name": name,
                "reason": "entity name not found in passage",
                })
                continue

            evidence_ok = exact_quote_is_supported(evidence, body)
            if not evidence_ok:
                result_for_chunk["rejected"].append({
                    "kind": "entity",
                    "name": name,
                    "reason": "evidence quote missing or not found verbatim",
                })
                continue

            key = normalize_name(name)
            record = {
                "name": name,
                "type": entity_type,
                "evidence": evidence.strip(),
                "source": source,
                "page": page,
                "chunk_id": chunk_id,
                "review_status": "needs_human_review",
            }

            # If a name appears with conflicting types, keep both candidates
            # in the report rather than silently selecting one.
            type_key = (key, entity_type)
            chunk_entities[type_key] = record
            candidate_entities[type_key] = candidate_entities.get(type_key, record)

        raw_relationships = data.get("relationships", [])
        if not isinstance(raw_relationships, list):
            raw_relationships = []

        for item in raw_relationships:
            if not isinstance(item, dict):
                continue

            source_name = item.get("source")
            relation_type = item.get("relationship")
            target_name = item.get("target")
            evidence = item.get("evidence", "")

            if not all(isinstance(value, str) for value in
                       [source_name, relation_type, target_name]):
                continue

            source_name = source_name.strip()
            target_name = target_name.strip()
            relation_type = relation_type.strip()

            if relation_type not in ALLOWED_RELATIONSHIPS:
                result_for_chunk["rejected"].append({
                    "kind": "relationship",
                    "source": source_name,
                    "relationship": relation_type,
                    "target": target_name,
                    "reason": "disallowed relationship type",
                })
                continue

            if normalize_name(source_name) == normalize_name(target_name):
                result_for_chunk["rejected"].append({
                    "kind": "relationship",
                    "source": source_name,
                    "relationship": relation_type,
                    "target": target_name,
                    "reason": "self-relationship rejected",
                })
                continue

            source_entity = next(
                (e for e in chunk_entities.values()
                 if normalize_name(e["name"]) == normalize_name(source_name)),
                None,
            )
            target_entity = next(
                (e for e in chunk_entities.values()
                 if normalize_name(e["name"]) == normalize_name(target_name)),
                None,
            )

            if source_entity is None or target_entity is None:
                result_for_chunk["rejected"].append({
                    "kind": "relationship",
                    "source": source_name,
                    "relationship": relation_type,
                    "target": target_name,
                    "reason": "endpoint not present among validated entities",
                })
                continue

            allowed_pairs = RELATIONSHIP_RULES.get(relation_type, set())
            endpoint_types = (source_entity["type"], target_entity["type"])
            if endpoint_types not in allowed_pairs:
                result_for_chunk["rejected"].append({
                    "kind": "relationship",
                    "source": source_name,
                    "relationship": relation_type,
                    "target": target_name,
                    "reason": f"endpoint types not allowed: {endpoint_types}",
                    })
                continue

            if not exact_quote_is_supported(evidence, body):
                result_for_chunk["rejected"].append({
                    "kind": "relationship",
                    "source": source_name,
                    "relationship": relation_type,
                    "target": target_name,
                    "reason": "relationship evidence quote missing or not found verbatim",
                })
                continue

            relation_key = (
                normalize_name(source_name),
                relation_type,
                normalize_name(target_name),
            )
            relation_record = {
                "source": source_entity["name"],
                "relationship": relation_type,
                "target": target_entity["name"],
                "evidence": evidence.strip(),
                "document": source,
                "page": page,
                "chunk_id": chunk_id,
                "review_status": "needs_human_review",
            }

            result_for_chunk["relationships"].append(relation_record)
            candidate_relationships.setdefault(relation_key, relation_record)

        result_for_chunk["entities"] = list(chunk_entities.values())
        chunk_results.append(result_for_chunk)
        print(
            f"  accepted entities: {len(result_for_chunk['entities'])}; "
            f"accepted relationships: {len(result_for_chunk['relationships'])}; "
            f"rejected candidates: {len(result_for_chunk['rejected'])}"
        )

    # Build a JSON report with evidence and rejection reasons.
    report = {
        "model": MODEL,
        "source_filter": ALLOWED_SOURCE,
        "category_filter": ALLOWED_CATEGORY,
        "chunks_selected": len(selected_chunks),
        "chunks_failed": len(failures),
        "entities": list(candidate_entities.values()),
        "relationships": list(candidate_relationships.values()),
        "failures": failures,
        "chunk_results": chunk_results,
        "important_note": (
            "Candidates have not been inserted into Neo4j. Exact evidence "
            "and type checks reduce errors but do not guarantee truth. "
            "Review every candidate before database insertion."
        ),
    }

    json_path = OUTPUT_DIR / "entity_extraction_report.json"
    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Readable text report, including accepted candidates and rejection totals.
    lines = [
        "IKS-Connect entity extraction report",
        f"Model: {MODEL}",
        f"Source filter: {ALLOWED_SOURCE}",
        f"Chunks selected: {len(selected_chunks)}",
        f"Chunks failed: {len(failures)}",
        "",
        "CANDIDATE ENTITIES (all require human review)",
    ]
    for entity in candidate_entities.values():
        lines.append(
            f'- {entity["type"]}: {entity["name"]} | '
            f'{entity["source"]}, page {entity["page"]}, '
            f'chunk {entity["chunk_id"]} | evidence: {entity["evidence"]}'
        )

    lines.extend(["", "CANDIDATE RELATIONSHIPS (all require human review)"])
    for relation in candidate_relationships.values():
        lines.append(
            f'- {relation["source"]} --{relation["relationship"]}--> '
            f'{relation["target"]} | {relation["document"]}, '
            f'page {relation["page"]}, chunk {relation["chunk_id"]} | '
            f'evidence: {relation["evidence"]}'
        )

    lines.extend(["", "REJECTIONS"])
    rejection_count = 0
    for chunk_result in chunk_results:
        for rejected in chunk_result.get("rejected", []):
            rejection_count += 1
            lines.append(
                f'- chunk {chunk_result["chunk_id"]}: '
                f'{json.dumps(rejected, ensure_ascii=False)}'
            )
    lines.extend([
        "",
        f"Rejected candidate count: {rejection_count}",
        "",
        "Nothing was inserted into Neo4j.",
        "Every accepted candidate still requires human review.",
    ])

    text_path = OUTPUT_DIR / "entity_extraction_report.txt"
    text_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print(f"Chunks selected: {len(selected_chunks)}")
    print(f"Chunks failed: {len(failures)}")
    print(f"Unique candidate entities: {len(candidate_entities)}")
    print(f"Unique candidate relationships: {len(candidate_relationships)}")
    print(f"JSON report: {json_path}")
    print(f"Readable report: {text_path}")
    print("Nothing was inserted into Neo4j.")
    print("=" * 60)


if __name__ == "__main__":
    main()
