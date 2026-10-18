
import faiss
import pickle
import requests

from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase


# -----------------------------
# 1. Configuration
# -----------------------------

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "IKSConnect123"
NEO4J_DATABASE = "iks"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

INDEX_PATH = "data/chunks/kerala/kerala.index"
EMBEDDINGS_PATH = "data/chunks/kerala/embeddings.pkl"


# -----------------------------
# 2. Load FAISS and embeddings
# -----------------------------

print("Loading document search...")

index = faiss.read_index(INDEX_PATH)

with open(EMBEDDINGS_PATH, "rb") as file:
    data = pickle.load(file)

chunks = data["chunks"]

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Document search ready.")


# -----------------------------
# 3. Search Neo4j
# -----------------------------

def search_graph(question):
    results = []

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    try:
        with driver.session(database=NEO4J_DATABASE) as session:

            # Search for graph facts related to the question.
            query = """
            MATCH (place:HeritageSite)-[r:LOCATED_IN]->(district:District)
            RETURN place.name AS place,
                   district.name AS district,
                   r.source AS source,
                   r.page AS page
            """

            records = session.run(query)

            question_words = set(
                question.lower().replace("?", "").split()
            )

            for record in records:
                place = record["place"]
                district = record["district"]

                fact_words = set(
                    (place + " " + district).lower().split()
                )

                # Include facts whose names overlap with the question.
                if (
                    question_words.intersection(fact_words)
                    or "museum" in question.lower()
                    or "gallery" in question.lower()
                    or "heritage" in question.lower()
                    or "district" in question.lower()
                    or "located" in question.lower()
                    or "where" in question.lower()
                ):
                    results.append({
                        "fact": f"{place} is located in {district}.",
                        "source": record["source"],
                        "page": record["page"]
                    })

    finally:
        driver.close()

    return results


# -----------------------------
# 4. Search FAISS documents
# -----------------------------

def search_documents(question, number_of_results=5):
    question_embedding = model.encode([question])

    distances, indices = index.search(
        question_embedding,
        number_of_results
    )

    results = []

    for i in range(len(indices[0])):
        chunk_index = int(indices[0][i])

        if chunk_index < 0 or chunk_index >= len(chunks):
            continue

        results.append(chunks[chunk_index])

    return results


# -----------------------------
# 5. Ask a question
# -----------------------------

question = input(
    "\nAsk a question about Kerala: "
).strip()

if not question:
    print("Please enter a question.")
    raise SystemExit


# Retrieve information from both sources.
print("\nSearching the knowledge graph...")
graph_results = search_graph(question)

print("Searching the documents...")
document_results = search_documents(question)


# -----------------------------
# 6. Combine context and citations
# -----------------------------

context_parts = []
citations = []

for item in graph_results:
    context_parts.append(
        "[KNOWLEDGE GRAPH]\n" + item["fact"]
    )

    if item["source"] and item["page"] is not None:
        citation = (
            f'{item["source"]}, page {item["page"]}'
        )

        if citation not in citations:
            citations.append(citation)

for i, chunk in enumerate(document_results, start=1):
    context_parts.append(
        f"[DOCUMENT PASSAGE {i}]\n{chunk}"
    )

context = "\n\n".join(context_parts)

if not context.strip():
    context = "No relevant information was retrieved."


# -----------------------------
# 7. Generate a grounded answer
# -----------------------------

prompt = f"""
You are IKS-Connect, an assistant for Kerala's cultural
heritage and traditional knowledge.

Answer the question using only the evidence provided below.

Rules:
- Do not invent facts, locations, or source details.
- Distinguish knowledge graph facts from document passages.
- If the evidence is insufficient, say so clearly.
- Do not claim that a source supports a fact unless it is
  explicitly present in the evidence.
- Give a concise, direct answer.

Evidence:
{context}

Question:
{question}

Answer:
"""

print("\nGenerating answer with Llama 3.2...")

try:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    result = response.json()

except requests.exceptions.RequestException as error:
    print("\nCould not contact Ollama.")
    print("Check that Ollama is running.")
    print("Details:", error)
    raise SystemExit(1)


# -----------------------------
# 8. Display answer and sources
# -----------------------------

print("\n" + "=" * 50)
print("IKS-CONNECT ANSWER")
print("=" * 50)

print(result.get("response", "No answer was generated."))

print("\n" + "-" * 50)
print("RETRIEVED SOURCES")
print("-" * 50)

if citations:
    for citation in citations:
        print("- " + citation)

if document_results:
    print("- Retrieved document passages from the FAISS index.")
    print(
        "  Note: individual document citations are not yet "
        "mapped to source filenames and page numbers."
    )

if not citations and not document_results:
    print("No sources were retrieved.")

print("\nDone.")
