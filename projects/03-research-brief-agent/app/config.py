import os


def get_config() -> dict[str, str | float]:
    return {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "timeout": float(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
    }

