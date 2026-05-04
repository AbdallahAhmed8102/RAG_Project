from qdrant_client import QdrantClient
from qdrant_client.http import models
from pymongo import MongoClient
import uuid 

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["robotics_docs"]
collection = db["documentation"]


qdrant_client = QdrantClient(host="localhost", port=6333)

if not qdrant_client.collection_exists("robotics_embeddings"):
    qdrant_client.create_collection(
        collection_name="robotics_embeddings",
        vectors_config=models.VectorParams(size=384, distance="Cosine")
    )
else:
    print("Collection 'robotics_embeddings' already exists. Skipping creation.")

documents = list(collection.find())

points = [
    models.PointStruct(
        id=str(uuid.uuid4()),  
        vector=doc["embedding"],
        payload={"content": doc["content"]}
    )
    for doc in documents if "embedding" in doc and doc["embedding"] 
]

if points:
    qdrant_client.upsert(collection_name="robotics_embeddings", points=points)
    print("Embeddings successfully transferred to Qdrant!")
else:
    print("No embeddings found to transfer to Qdrant.")
