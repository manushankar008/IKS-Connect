import re

input_path = "data/extracted/kerala/kerala_economic_review_2024_clean.txt"
output_path = "data/chunks/kerala/kerala_chunks.txt"

with open(input_path, "r", encoding="utf-8") as file:
    text = file.read()

# Split the document into pages
pages = re.split(r"--- PAGE (\d+) ---", text)

chunks = []

chunk_size = 1500
overlap = 200

for i in range(1, len(pages), 2):

    page_number = pages[i]
    page_text = pages[i + 1].strip()

    if not page_text:
        continue

    # Split page text into smaller pieces
    start = 0

    while start < len(page_text):

        end = start + chunk_size
        chunk_text = page_text[start:end]

        chunks.append({
            "page": page_number,
            "text": chunk_text
        })

        start = end - overlap


# Save chunks
with open(output_path, "w", encoding="utf-8") as file:

    for i, chunk in enumerate(chunks):

        file.write(f"\n--- CHUNK {i} ---\n")
        file.write(f"PAGE: {chunk['page']}\n")
        file.write(chunk["text"])
        file.write("\n")


print("Text chunked successfully!")
print("Number of chunks:", len(chunks))