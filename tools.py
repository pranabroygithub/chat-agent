from langchain.tools import tool
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call
from models import GetDocumentRequest
from database import DBManager
from initialize import init_logger

logger = init_logger()

@tool(args_schema=GetDocumentRequest)
def get_rag_data_for_agent( query: str,
                            collection_name: str,
                            limit: int,
                            metadata: dict
                            ):
    """Get documents from RAG datastore for more context"""
    db_manager = DBManager(collection_name)
    results = db_manager.get_documents(query, limit, metadata if metadata else None)
    return results

@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

