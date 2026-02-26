from fastapi import FastAPI
from models import ChatRequest, DocumentRequest
from llm import chat
from initialize import init_llm, init_logger
from database import DBManager


app = FastAPI()
logger = init_logger()


@app.post("/chat")
def chat_with_agent(chat_request: ChatRequest):
    logger.info(f"{chat_request.model_dump()}")
    llm_response = chat(chat_request, init_llm(chat_request.chat_options))
    return llm_response.content


@app.post("/document")
def add_document(document: DocumentRequest):
    db_manager = DBManager(document)
    doc_id = db_manager.add_document(document.document, document.metadata)
    return doc_id

