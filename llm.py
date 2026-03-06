from models import ChatRequest
from langchain.agents import create_agent
from initialize import init_logger
from tools import get_customer_data, handle_tool_errors
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage, AIMessage, ToolMessage

logger = init_logger()

def chat(chat_request: ChatRequest, model: ChatOllama):
    logger.debug(f"model = {model.model_dump()}")
    messages = [
        ("system", chat_request.system_prompt),
        ("human",  chat_request.user_prompt)
    ]
    result = model.invoke(messages)
    logger.debug(f"LLM response = {result}")
    return result


def agent_chat(chat_request: ChatRequest, model: ChatOllama):
    agent = create_agent(
                model,
                tools=[get_customer_data],
                system_prompt=chat_request.system_prompt,
                middleware=[handle_tool_errors],
                response_format=chat_request.response_format,
                checkpointer=InMemorySaver()
            )
    result = agent.invoke(
                {"messages": [{"role": "user", "content": chat_request.user_prompt}]},
                {"configurable": {"thread_id": "1"}}
            )
    #logger.debug(f"Agent response = {result}")
    format_agent_response(result)
    return result

def format_agent_response(agent_response):
    messages = agent_response.get("messages")
    for message in messages:
        if(isinstance(message, HumanMessage)):
            logger.info(f"{'=' * 30} HumanMessage {'=' * 30}")
            logger.info(message.content)
        if(isinstance(message, AIMessage)):
            logger.info(f"{'=' * 30} AIMessage {'=' * 30}")
            if message.content:
                logger.info(message.content)
            if message.additional_kwargs.get("reasoning_content"):
                logger.info(f"{'=' * 30} Reason {'=' * 30}")
                logger.info(message.additional_kwargs.get("reasoning_content"))
        if(isinstance(message, ToolMessage)):
            logger.info(f"{'=' * 30} ToolMessage {'=' * 30}")
            if message.content:
                logger.info(message.content)
            if message.additional_kwargs.get("reasoning_content"):
                logger.info(f"{'=' * 30} Reason {'=' * 30}")
                logger.info(message.additional_kwargs.get("reasoning_content"))

