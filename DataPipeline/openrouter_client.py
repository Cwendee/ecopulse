import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests


@dataclass
class OpenRouterConfig:
    base_url: str
    api_key: Optional[str]
    model: str
    site_url: Optional[str] = None
    site_name: Optional[str] = None
    timeout: float = 30.0


def default_config() -> OpenRouterConfig:
    base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    # Using openai/gpt-4o-mini as clarified by the user
    model = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    site_url = os.environ.get("OPENROUTER_SITE_URL")
    site_name = os.environ.get("OPENROUTER_SITE_NAME", "EcoPulse")
    return OpenRouterConfig(
        base_url=base_url, 
        api_key=api_key, 
        model=model, 
        site_url=site_url, 
        site_name=site_name
    )


def generate(prompt: str, config: Optional[OpenRouterConfig] = None) -> str:
    cfg = config or default_config()
    url = cfg.base_url.rstrip("/") + "/chat/completions"
    
    headers: Dict[str, str] = {
        "Content-Type": "application/json",
    }
    
    if cfg.api_key:
        headers["Authorization"] = f"Bearer {cfg.api_key}"
    
    # OpenRouter optional headers
    if cfg.site_url:
        headers["HTTP-Referer"] = cfg.site_url
    if cfg.site_name:
        headers["X-Title"] = cfg.site_name

    payload: Dict[str, Any] = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": "You are a precise humanitarian and data assistant for EcoPulse."},
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
        raise RuntimeError("Unexpected response format from OpenRouter service")
    
    return content
