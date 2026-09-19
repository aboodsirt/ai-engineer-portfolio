import httpx


class LLMClient:
    def __init__(self, config: dict[str, str | float]) -> None:
        self.base_url = str(config["openai_base_url"]).rstrip("/")
        self.api_key = str(config["openai_api_key"])
        self.model = str(config["openai_model"])
        self.embedding_model = str(config["embedding_model"])
        self.timeout = float(config["timeout"])

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = httpx.post(
            f"{self.base_url}/embeddings",
            headers=self._headers(),
            json={"model": self.embedding_model, "input": texts},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return [item["embedding"] for item in response.json()["data"]]

    def chat(self, system: str, user: str) -> str:
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=self._headers(),
            json={
                "model": self.model,
                "temperature": 0.1,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
