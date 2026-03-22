from models import ChatRequest, AgentWithRagRequest
from langchain.agents import create_agent
from initialize import init_logger
from tools import handle_tool_errors, get_rag_data_for_agent
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


def agent_chat(agent_with_rag_request: AgentWithRagRequest, model: ChatOllama):
    document_request = agent_with_rag_request.document_request
    agent_request = agent_with_rag_request.agent_request
    agent = create_agent(
                model,
                tools = [get_rag_data_for_agent],
                system_prompt = agent_request.system_prompt,
                middleware = [handle_tool_errors],
                response_format = agent_request.response_format,
                checkpointer=InMemorySaver()
            )
    messages=[]
    messages.append({"role": "user", "content": agent_request.user_prompt})
    if document_request:
        messages.append({"role": "user", "content": f"For more context use get documents using: {document_request.model_dump()}."})
    result = agent.invoke(
                {"messages": messages},
                {"configurable": {"thread_id": "1"}}
            )
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

