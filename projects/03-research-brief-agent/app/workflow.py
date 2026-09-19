import asyncio
import json
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


@dataclass
class SourceNote:
    source_id: str
    url: str
    text: str
    error: str | None = None


def clean_html(html: str, limit: int = 12000) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript", "svg"]):
        node.decompose()
    return " ".join(soup.get_text(" ").split())[:limit]


def valid_public_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}


class ResearchWorkflow:
    def __init__(self, config: dict[str, str | float]) -> None:
        self.base_url = str(config["base_url"]).rstrip("/")
        self.api_key = str(config["api_key"])
        self.model = str(config["model"])
        self.timeout = float(config["timeout"])

    async def run(self, question: str, urls: list[str]) -> dict[str, object]:
        safe_urls = [url for url in urls if valid_public_url(url)]
        plan = self.plan(question, safe_urls)
        notes = await asyncio.gather(*(self.fetch_source(f"S{index + 1}", url) for index, url in enumerate(safe_urls)))
        evidence = "\n\n".join(f"[{note.source_id}] {note.url}\n{note.text or note.error}" for note in notes)
        brief = self.synthesize(question, plan, evidence)
        return {"brief": brief, "plan": plan, "sources": [note.__dict__ for note in notes]}

    def plan(self, question: str, urls: list[str]) -> list[str]:
        prompt = json.dumps({"question": question, "sources": urls})
        result = self.complete(
            "You are the planning agent. Return valid JSON with a single key named research_questions containing an array of three concise questions.",
            prompt,
        )
        try:
            questions = json.loads(result).get("research_questions", [])
            return [str(item) for item in questions[:3]]
        except (json.JSONDecodeError, AttributeError):
            return [question]

    async def fetch_source(self, source_id: str, url: str) -> SourceNote:
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(url, headers={"User-Agent": "ai-engineer-portfolio/1.0"})
                response.raise_for_status()
            return SourceNote(source_id, url, clean_html(response.text))
        except httpx.HTTPError as error:
            return SourceNote(source_id, url, "", str(error))

    def synthesize(self, question: str, plan: list[str], evidence: str) -> str:
        return self.complete(
            "You are the synthesis agent. Write a concise research brief with a summary, key findings, tradeoffs, and a source list. Every factual claim must include a source label such as [S1]. Say when evidence is missing.",
            f"Question: {question}\nResearch questions: {json.dumps(plan)}\nEvidence:\n{evidence}",
        )

    def complete(self, system: str, user: str) -> str:
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "temperature": 0.2, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

