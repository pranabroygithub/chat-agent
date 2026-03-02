from pydantic import BaseModel
from typing import Any
from uuid import uuid4

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

class AddDocumentRequest(BaseModel):
    collection_name: str
    metadata: dict = {}
    document: Any
    limit: int = 5

class GetDocumentRequest(BaseModel):
    query: str
    collection_name: str
    metadata: dict = {}
    limit: int = 5
