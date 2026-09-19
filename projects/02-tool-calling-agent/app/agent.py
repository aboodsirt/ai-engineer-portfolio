import json
from typing import Any

import httpx

from .tools import TOOL_DEFINITIONS, TOOL_HANDLERS


class ToolCallingAgent:
    def __init__(self, config: dict[str, str | float], max_steps: int = 6) -> None:
        self.base_url = str(config["base_url"]).rstrip("/")
        self.api_key = str(config["api_key"])
        self.model = str(config["model"])
        self.timeout = float(config["timeout"])
        self.max_steps = max_steps

    def run(self, message: str) -> dict[str, Any]:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": "You are a concise support operations assistant. Use tools for arithmetic and policy facts. Never invent tool results."},
            {"role": "user", "content": message},
        ]
        trace = []
        for step in range(self.max_steps):
            response = self._complete(messages)
            choice = response["choices"][0]
            assistant = choice["message"]
            messages.append(assistant)
            calls = assistant.get("tool_calls", [])
            if not calls:
                return {"answer": assistant.get("content", ""), "steps": step + 1, "trace": trace}
            for call in calls:
                name = call["function"]["name"]
                arguments = json.loads(call["function"].get("arguments") or "{}")
                if name not in TOOL_HANDLERS:
                    result = "Unknown tool"
                else:
                    try:
                        result = TOOL_HANDLERS[name](arguments)
                    except ValueError as error:
                        result = f"Invalid tool arguments: {error}"
                trace.append({"tool": name, "arguments": arguments, "result": result})
                messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
        raise RuntimeError("Agent exceeded its tool-call step limit")

    def _complete(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "temperature": 0.1, "messages": messages, "tools": TOOL_DEFINITIONS, "tool_choice": "auto"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

