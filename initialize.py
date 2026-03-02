from langchain_ollama import ChatOllama
from config import settings
from models import ChatModelOptions
import logging
from loggers import LOGGING_CONFIG


def init_llm(options: ChatModelOptions):
    llm = ChatOllama(
        base_url = settings.ollama_url,
        model = settings.ollama_chat_model,
        reasoning = options.reasoning
    )
    return llm


def init_logger(profile: str = "main-server"):
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(profile)
    return logger
