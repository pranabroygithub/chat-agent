from pydantic import BaseModel
from typing import Any
from uuid import uuid4
from config import settings

class ChatModelOptions(BaseModel):
    reasoning : bool = False

class ChatRequest(BaseModel):
    user_prompt: str
    system_prompt: str
    chat_options: ChatModelOptions = ChatModelOptions()

class Document(BaseModel):
    doc_id: uuid4
    document: Any
    embeddings: float

class DocumentRequest(BaseModel):
    chroma_db_path: str = settings.chroma_db_path
    collection_name: str
    ollama_embedding_model: str = settings.ollama_embedding_model
    metadata: dict = {}
    document: Any
    ollama_embedding_url : str = settings.ollama_embedding_url
