from fastapi import FastAPI
from pydantic import BaseModel, Field

from .config import get_config
from .workflow import ResearchWorkflow

app = FastAPI(title="Research Brief Agent", version="1.0.0")
workflow = ResearchWorkflow(get_config())


class BriefRequest(BaseModel):
    question: str = Field(min_length=8, max_length=1000)
    sources: list[str] = Field(min_length=1, max_length=8)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/brief")
async def brief(request: BriefRequest) -> dict[str, object]:
    return await workflow.run(request.question, request.sources)

