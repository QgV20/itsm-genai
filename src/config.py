
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SEED = 42

EMB_MODEL = "intfloat/multilingual-e5-small"

LLM_MODEL = "qwen2.5:3b"

OLLAMA_URL = "http://localhost:11434/api/chat"
