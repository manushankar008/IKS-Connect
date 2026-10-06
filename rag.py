import faiss
import pickle
from sentence_transformers import SentenceTransformer
import requests


# Load FAISS index
index = faiss.read_index("data/chunks/kerala/kerala.index")


# Load chunks
with open("data/chunks/kerala/embeddings.pkl", "rb") as file:
    data = pickle.load(file)

chunks = data["chunks"]


# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Ask the user for a question
question = input("Ask a question about Kerala: ")


# Convert the question into an embedding
question_embedding = model.encode([question])


# Search FAISS for the 5 most relevant chunks
distances, indices = index.search(question_embedding, 5)


# Create context from the retrieved chunks
context = ""

for i in range(5):
    context += chunks[indices[0][i]]
    context += "\n\n"


# Create the prompt for Llama
prompt = f"""
You are a Kerala cultural heritage assistant.

Answer the user's question using only the information provided in the context below.

If the context does not contain enough information to answer the question, say:
"I don't have enough information in my current sources to answer that."

Do not make up facts.

Context:
{context}

Question:
{question}

Answer:
"""


# Send the prompt to Ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
)


# Get the answer
result = response.json()


# Display the answer
print("\nAnswer:\n")
print(result["response"])