from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    expression: str = Field(min_length=1, max_length=100)


class KnowledgeInput(BaseModel):
    topic: str = Field(min_length=2, max_length=120)


class TimeInput(BaseModel):
    timezone: str = "UTC"


def calculate(arguments: dict[str, Any]) -> str:
    data = CalculatorInput.model_validate(arguments)
    allowed = set("0123456789+-*/(). ")
    if not set(data.expression) <= allowed:
        return "Only arithmetic expressions are supported"
    try:
        result = eval(data.expression, {"__builtins__": {}}, {})
    except (ArithmeticError, SyntaxError, ValueError):
        return "The expression could not be evaluated"
    return str(result)


def search_knowledge(arguments: dict[str, Any]) -> str:
    data = KnowledgeInput.model_validate(arguments)
    entries = {
        "payment": "Payment disputes are priority one and should be escalated with the customer identifier, timeline, troubleshooting steps, and desired outcome.",
        "security": "Account security issues require immediate escalation to the trust and safety queue.",
        "refund": "Monthly subscriptions can be refunded within fourteen days when usage remains below the fair-use threshold.",
    }
    topic = data.topic.lower()
    matches = [value for key, value in entries.items() if key in topic]
    return " ".join(matches) if matches else "No matching support policy was found"


def current_time(arguments: dict[str, Any]) -> str:
    TimeInput.model_validate(arguments)
    return datetime.now(UTC).isoformat()


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a basic arithmetic expression without access to Python or the filesystem.",
            "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Look up a support policy by topic.",
            "parameters": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "current_time",
            "description": "Get the current UTC timestamp.",
            "parameters": {"type": "object", "properties": {"timezone": {"type": "string"}}},
        },
    },
]

TOOL_HANDLERS = {"calculate": calculate, "search_knowledge": search_knowledge, "current_time": current_time}

