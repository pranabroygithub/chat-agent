from fastapi import APIRouter
from models import ChatRequest
from llm import chat
from initialize import init_llm, init_logger


logger = init_logger()

router = APIRouter(prefix="/agent")

@router.post("/chat")
def chat_with_agent(chat_request: ChatRequest):
    logger.info(f"request_body: {chat_request}")
    llm_response = chat(chat_request, init_llm(chat_request.chat_options))
    return llm_response.content
