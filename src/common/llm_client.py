
import hashlib
import json

import requests

from src.config import ROOT, LLM_MODEL, OLLAMA_URL

CACHE = ROOT / "data" / "llm_cache.jsonl"
_cache = {}


def load_cache():
    if not CACHE.exists():
        return

    with CACHE.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            item = json.loads(line)
            _cache[item["k"]] = item["v"]


load_cache()


def ask_llm(messages, json_mode=False, model=LLM_MODEL):
    key_data = json.dumps(
        [messages, json_mode, model],
        ensure_ascii=False,
        sort_keys=True,
    )

    key = hashlib.md5(key_data.encode("utf-8")).hexdigest()

    # Đã có kết quả thì dùng lại, không gọi model lần nữa
    if key in _cache:
        return _cache[key]

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0},
    }

    if json_mode:
        payload["format"] = "json"

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300,
    )
    response.raise_for_status()

    output = response.json()["message"]["content"]

    CACHE.parent.mkdir(parents=True, exist_ok=True)

    with CACHE.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {"k": key, "v": output},
                ensure_ascii=False,
            ) + "\n"
        )

    _cache[key] = output

    return output
