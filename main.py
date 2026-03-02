from fastapi import FastAPI
from routers import rag, agent

app = FastAPI()

app.include_router(agent.router)
app.include_router(rag.router)


app.get("/")
async def root():
    return({"message": "Welcome to langchain agent with rag"})
