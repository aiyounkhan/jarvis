import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime
import uuid

class VectorStore: 
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/chroma_db")
        self.collection = self.client.get_or_create_collection(name="jarvis_memory")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    def save(self, text, metadata={}):
        embedding = self.embedder.encode(text).tolist()
        self.collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                **metadata
            }]
        )
    
    def search(self, query, n_results=5):
        embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []