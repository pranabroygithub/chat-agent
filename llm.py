from models import ChatRequest, ChatModelOptions
from initialize import init_logger


logger = init_logger()

def chat(chat_request: ChatRequest, llm: ChatModelOptions):
    logger.debug(f"llm = {llm.model_dump()}")
    messages = [
        ("system", chat_request.system_prompt),
        ("human",  chat_request.user_prompt)
    ]
    llm_msg = llm.invoke(messages)
    logger.debug(f"llm response = {llm_msg}")
    return llm_msg
