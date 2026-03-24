from pydantic import BaseModel
from typing import Any, Optional
from uuid import uuid4

class ChatModelOptions(BaseModel):
    reasoning : bool = False
    collection_name: str = ""

class ChatRequest(BaseModel):
    user_prompt: str
    system_prompt: str
    response_format: Any = None
    chat_options: ChatModelOptions = ChatModelOptions()

class Document(BaseModel):
    id: uuid4
    document: Any
    embeddings: float

class AddDocumentRequest(BaseModel):
    collection_name: str
    document: Any
    limit: int = 5
    metadata: dict = {}

class UpdateDocumentRequest(BaseModel):
    id: str
    collection_name: str
    document: Any
    metadata: dict

class GetDocumentRequest(BaseModel):
    query: str
    collection_name: str
    limit: int = 5
    metadata: dict = {}

class AgentWithRagRequest(BaseModel):
    document_request: Optional[GetDocumentRequest] = None
    agent_request: ChatRequest
