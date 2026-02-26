from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import chromadb
from models import DocumentRequest
from uuid import uuid4
from initialize import init_logger


logger = init_logger()

class DBManager:
    def __init__(self, document: DocumentRequest):
        self.client = chromadb.PersistentClient(path=document.chroma_db_path)

        self.embeddings = OllamaEmbeddings(
            model = document.ollama_embedding_model,
            base_url = document.ollama_embedding_url
        )

        self.vector_store = Chroma(
            client = self.client,
            collection_name = document.collection_name,
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
