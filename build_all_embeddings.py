import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


input_path = "data/chunks/kerala/kerala_chunks.txt"
output_path = "data/chunks/kerala/embeddings.pkl"


# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Read all chunks
with open(input_path, "r", encoding="utf-8") as file:
    text = file.read()


# Split into individual chunks
chunks = text.split("--- CHUNK ")

chunks = [
    chunk.strip()
    for chunk in chunks
    if chunk.strip()
]


print("Number of chunks:", len(chunks))


# Create embeddings
print("\nCreating embeddings...")

embeddings = model.encode(
    chunks,
    show_progress_bar=True
)


# Convert to numpy array
embeddings = np.array(embeddings)


# Save everything together
data = {
    "chunks": chunks,
    "embeddings": embeddings
}


with open(output_path, "wb") as file:
    pickle.dump(data, file)


print("\nEmbeddings created successfully!")
print("Number of chunks:", len(chunks))
print("Embedding size:", embeddings.shape)
print("Saved:", output_path)