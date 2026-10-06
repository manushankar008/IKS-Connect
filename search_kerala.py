import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load FAISS index
index = faiss.read_index("data/chunks/kerala/kerala.index")

# Load chunks
with open("data/chunks/kerala/embeddings.pkl", "rb") as file:
    data = pickle.load(file)

chunks = data["chunks"]

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Ask a question
question = "What is Kerala known for in terms of art and culture?"

# Convert question into embedding
question_embedding = model.encode([question])

# Search for the 5 most relevant chunks
distances, indices = index.search(question_embedding, 5)

# Display results
for i in range(5):

    print("\n-----------------------------")
    print("Result:", i + 1)
    print("Distance:", distances[0][i])
    print(chunks[indices[0][i]])