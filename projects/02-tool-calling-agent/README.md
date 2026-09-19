# Tool Calling Agent

A support operations agent that lets an LLM choose between deterministic tools, execute them safely, and continue the conversation until it can answer the user.

The loop supports multiple tool calls, validates arguments with Pydantic, keeps tool results in the message history, and exposes a small HTTP API.

## Run

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Example request:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/chat -ContentType 'application/json' -Body '{"message":"Calculate the refund for 3 months at 19.99 and tell me the escalation target for a payment dispute."}'
```

