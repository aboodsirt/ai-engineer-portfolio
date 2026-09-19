install:
	pip install -r projects/01-rag-knowledge-base/requirements.txt

test:
	python -m pytest projects/02-tool-calling-agent/tests
	python -m pytest projects/03-research-brief-agent/tests
	python -m pytest projects/04-llm-evaluation-harness/tests
	python -m pytest projects/05-llm-gateway/tests
	python -m pytest projects/06-voice-rag-assistant/tests
