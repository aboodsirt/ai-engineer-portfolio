from fastapi import FastAPI
from pydantic import BaseModel, Field

from .agent import ToolCallingAgent
from .config import get_config

app = FastAPI(title="Tool Calling Agent", version="1.0.0")
agent = ToolCallingAgent(get_config())


class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=4000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, object]:
    return agent.run(request.message)

