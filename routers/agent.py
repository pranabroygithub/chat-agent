from fastapi import APIRouter
from models import ChatRequest
from llm import chat, agent_chat
from initialize import init_llm, init_logger


logger = init_logger()

router = APIRouter(prefix="/agent")

@router.post("/chat")
def chat_with_agent(chat_request: ChatRequest):
    logger.info(f"request_body: {chat_request}")
    llm_response = chat(chat_request, init_llm(chat_request.chat_options))
    return llm_response.content


@router.post("/generate")
def generate_with_agent(chat_request: ChatRequest):
    logger.info(f"request_body: {chat_request}")
    agent_response = agent_chat(chat_request, init_llm(chat_request.chat_options))
    messages = agent_response.get("messages")
    final_response = messages[-1].content
    return final_response
