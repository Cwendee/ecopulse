import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests


@dataclass
class GPTOSSConfig:
    base_url: str
    api_key: Optional[str]
    model: str
    timeout: float = 30.0


def default_config() -> GPTOSSConfig:
    base_url = os.environ.get("GPT_OSS_BASE_URL", "http://localhost:8000/v1")
    api_key = os.environ.get("GPT_OSS_API_KEY")
    model = os.environ.get("GPT_OSS_MODEL", "gpt-oss")
    return GPTOSSConfig(base_url=base_url, api_key=api_key, model=model)


def generate(prompt: str, config: Optional[GPTOSSConfig] = None) -> str:
    cfg = config or default_config()
    url = cfg.base_url.rstrip("/") + "/chat/completions"
    headers: Dict[str, str] = {"Content-Type": "application/json"}
    if cfg.api_key:
        headers["Authorization"] = f"Bearer {cfg.api_key}"
    payload: Dict[str, Any] = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": "You are a precise classification and matching assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=cfg.timeout)
    resp.raise_for_status()
    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError("Unexpected response format from gpt-oss service")
    return content
