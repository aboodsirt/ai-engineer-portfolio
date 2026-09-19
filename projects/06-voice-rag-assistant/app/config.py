import os


def get_config() -> dict[str, str | float]:
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "openai_base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "embedding_model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        "elevenlabs_api_key": os.getenv("ELEVENLABS_API_KEY", ""),
        "elevenlabs_base_url": os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io/v1"),
        "stt_model": os.getenv("ELEVENLABS_STT_MODEL", "scribe_v2"),
        "tts_model": os.getenv("ELEVENLABS_TTS_MODEL", "eleven_flash_v2_5"),
        "voice_id": os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"),
        "timeout": float(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
    }
