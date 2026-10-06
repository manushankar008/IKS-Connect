import faiss
import pickle
from sentence_transformers import SentenceTransformer


index = faiss.read_index(
    "data/chunks/kerala/kerala.index"
)


with open(
    "data/chunks/kerala/embeddings.pkl",
    "rb"
) as file:
    data = pickle.load(file)


chunks = data["chunks"]


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


question = input("Ask a question about Kerala: ")


question_embedding = model.encode(
    [question]
)


distances, indices = index.search(
    question_embedding,
    5
)


for i in range(5):

    print("\n" + "=" * 60)

    print("RESULT:", i + 1)

    print("DISTANCE:", distances[0][i])

    print("\n")

    print(chunks[indices[0][i]])