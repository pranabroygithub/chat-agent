from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import chromadb
from uuid import uuid4
from initialize import init_logger
from config import settings


logger = init_logger()

class DBManager:
    def __init__(self, collection_name: str):
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)

        self.embeddings = OllamaEmbeddings(
            model = settings.ollama_embedding_model,
            base_url = settings.ollama_embedding_url
        )

        self.vector_store = Chroma(
            client = self.client,
            collection_name = collection_name,
            embedding_function = self.embeddings
        )

    def add_document(self, document: str, metadata: dict):
        doc_id = str(uuid4())
        doc = Document(
            page_content = document,
            metadata = metadata,
            id = doc_id
        )
        self.vector_store.add_documents(documents=[doc], ids=[doc_id])
        return {"doc_id" : doc_id}

    def get_documents(self, query: str, limit: int, metadata: dict):
        results = self.vector_store.similarity_search(
            query = query,
            k = limit,
            filter = metadata
        )
        return results

