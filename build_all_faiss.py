import faiss
import pickle


input_path = "data/chunks/kerala/embeddings.pkl"
output_path = "data/chunks/kerala/kerala.index"


# Load embeddings
with open(input_path, "rb") as file:
    data = pickle.load(file)


embeddings = data["embeddings"]


# Get embedding size
dimension = embeddings.shape[1]


# Create FAISS index
index = faiss.IndexFlatL2(dimension)


# Add embeddings
index.add(embeddings)


# Save index
faiss.write_index(index, output_path)


print("FAISS index created successfully!")
print("Number of vectors:", index.ntotal)
print("Dimension:", dimension)
print("Saved:", output_path)