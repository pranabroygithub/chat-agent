from langchain.tools import tool
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call

@tool
def get_customer_data(query: str) -> dict:
    """Search for customer information."""
    # A dictionary containing 10 customer records
    customers = {
        "C001": {"name": "Alice Johnson", "email": "alice@email.com", "balance": 150.50, "active": True},
        "C002": {"name": "Bob Smith", "email": "bob.s@provider.net", "balance": 0.00, "active": False},
        "C003": {"name": "Charlie Davis", "email": "charlie_d@webmail.com", "balance": 2400.75, "active": True},
        "C004": {"name": "Diana Prince", "email": "diana@themyscira.io", "balance": 890.20, "active": True},
        "C005": {"name": "Ethan Hunt", "email": "ethan.h@imf.org", "balance": 45.00, "active": True},
        "C006": {"name": "Fiona Gallagher", "email": "fiona.g@southside.com", "balance": 12.30, "active": False},
        "C007": {"name": "George Miller", "email": "george.m@studio.com", "balance": 560.00, "active": True},
        "C008": {"name": "Hannah Abbott", "email": "hannah.a@hogwarts.edu", "balance": 310.45, "active": True},
        "C009": {"name": "Ian Wright", "email": "ian.w@footballer.co.uk", "balance": 1200.00, "active": True},
        "C010": {"name": "Julia Roberts", "email": "julia.r@cinema.com", "balance": 9500.60, "active": True}
    }
    return customers

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

