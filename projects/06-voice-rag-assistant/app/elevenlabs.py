import httpx


class ElevenLabsClient:
    def __init__(self, config: dict[str, str | float]) -> None:
        self.base_url = str(config["elevenlabs_base_url"]).rstrip("/")
        self.api_key = str(config["elevenlabs_api_key"])
        self.stt_model = str(config["stt_model"])
        self.tts_model = str(config["tts_model"])
        self.voice_id = str(config["voice_id"])
        self.timeout = float(config["timeout"])

    def _headers(self) -> dict[str, str]:
        return {"xi-api-key": self.api_key}

    def transcribe(self, audio: bytes, filename: str, content_type: str) -> str:
        response = httpx.post(
            f"{self.base_url}/speech-to-text",
            headers=self._headers(),
            files={"file": (filename, audio, content_type)},
            data={"model_id": self.stt_model},
            timeout=self.timeout,
        )
        response.raise_for_status()
        text = str(response.json().get("text", "")).strip()
        if not text:
            raise ValueError("The audio did not contain a transcript")
        return text

    def synthesize(self, text: str) -> bytes:
        response = httpx.post(
            f"{self.base_url}/text-to-speech/{self.voice_id}",
            params={"output_format": "mp3_44100_128"},
            headers={**self._headers(), "Content-Type": "application/json"},
            json={"text": text, "model_id": self.tts_model},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.content
