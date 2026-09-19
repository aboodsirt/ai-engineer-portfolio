# Voice RAG Assistant

An end-to-end voice support assistant that accepts an audio message, transcribes it with ElevenLabs Scribe, retrieves grounded context from a local support handbook, generates an answer with an OpenAI-compatible chat API, and synthesizes the answer with ElevenLabs Text to Speech.

## Flow

1. Upload an audio file to the FastAPI endpoint.
2. ElevenLabs Scribe converts the speech to text.
3. The local handbook is searched with embedding cosine similarity.
4. The LLM answers only from the retrieved support context.
5. ElevenLabs returns an MP3 voice response.

## Run

```powershell
pip install -r requirements.txt
Copy-Item ..\..\.env.example .env
uvicorn app.main:app --reload
```

Index the knowledge base:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/ingest
```

Send an audio message:

```powershell
curl.exe -X POST http://127.0.0.1:8000/voice-query -F "audio=@question.mp3"
```

The response includes the transcript, grounded answer, source chunks, and base64-encoded MP3 audio in `audio_base64`.

## API

- `GET /health` returns service and index state.
- `POST /ingest` embeds the Markdown handbook.
- `POST /voice-query` accepts `wav`, `mp3`, `m4a`, `ogg`, or `webm` audio.

## Environment

Set `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, and the OpenAI-compatible LLM variables in `.env`. No provider keys are committed.
