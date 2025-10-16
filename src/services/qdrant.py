import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, PointIdsList
from src.config.qdrant import db_qdrant

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(**db_qdrant)

    def create_collection(self, collection_name: str):
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )
    
    def search_collection(self, collection_name: str, query_vector: np.ndarray, limit: int = 10):
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
        )

    def insert_vector(self, collection_name: str, point_id: str, vector: np.ndarray, payload: dict):
        return self.client.upsert(
            collection_name=collection_name,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)],
        )
    def delete_vector(self, collection_name: str, vector_id: str):
        self.client.delete(
            collection_name=collection_name,
            vector_id=vector_id,
        )