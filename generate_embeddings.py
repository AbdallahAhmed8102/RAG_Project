from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

def preprocess(text):
    """Basic preprocessing for text."""
    return text.strip().lower()

def fetch_data_from_mongo(collection):
    """Fetch documents from MongoDB."""
    return list(collection.find())

def generate_embeddings(texts, model):
    """Generate embeddings for a list of texts."""
    return [model.encode(text).tolist() for text in texts]

def update_embeddings_in_mongo(collection, documents, embeddings):
    """Update MongoDB documents with their corresponding embeddings."""
    for doc, embedding in zip(documents, embeddings):
        collection.update_one(
            {"_id": doc["_id"]},  
            {"$set": {"embedding": embedding}}  
        )

if __name__ == "__main__":
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["robotics_docs"]  
    collection = db["documentation"]  

    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    
    documents = fetch_data_from_mongo(collection)

    
    texts = [preprocess(doc["content"]) for doc in documents]  

    
    embeddings = generate_embeddings(texts, model)
    
    
    update_embeddings_in_mongo(collection, documents, embeddings)

    print("Embeddings generated and stored in MongoDB successfully!")
