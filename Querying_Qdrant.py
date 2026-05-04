from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient


qdrant_client = QdrantClient(host="localhost", port=6333)  


model = SentenceTransformer('all-MiniLM-L6-v2')


def search_qdrant(query, model, qdrant_client, collection_name="robotics_embeddings", top_k=5):
    """Search Qdrant for similar embeddings."""
    query_vector = model.encode(query).tolist()
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    return [result.payload["content"] for result in results]
query = "How does MoveIt2 handle motion planning?"
retrieved_docs = search_qdrant(query, model, qdrant_client)

print("Retrieved Documents:")
for doc in retrieved_docs:
    print(doc)
