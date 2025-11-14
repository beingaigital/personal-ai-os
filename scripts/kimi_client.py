import os
import json
from typing import List, Dict, Any, Optional

import time
import http.client
from urllib.parse import urlparse


class KimiClient:
    """
    Minimal Kimi API client.
    Uses simple stdlib HTTP to avoid external dependencies.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key_env: str = "KIMI_API_KEY",
        default_temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout_seconds: int = 60,
        endpoint_path: str = "/v1/chat/completions",
        request_format: str = "openai",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = os.getenv(api_key_env, "")
        self.default_temperature = default_temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        self.endpoint_path = endpoint_path
        self.request_format = request_format
        if not self.api_key:
            raise RuntimeError(f"Environment variable {api_key_env} is not set.")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        retries: int = 3,
        retry_delay_seconds: float = 2.0,
    ) -> str:
        temp_value = temperature if temperature is not None else self.default_temperature
        max_tokens_value = max_output_tokens if max_output_tokens is not None else self.max_tokens
        if self.request_format == "openai":
            body = {
                "model": self.model,
                "messages": messages,
                "temperature": temp_value,
                "max_tokens": max_tokens_value,
            }
        else:
            body = {
                "model": self.model,
                "input": messages,
                "parameters": {
                    "temperature": temp_value,
                    "max_output_tokens": max_tokens_value,
                },
            }
        endpoint = f"{self.base_url}{self.endpoint_path}"
        url = urlparse(endpoint)
        is_https = url.scheme == "https"
        for attempt in range(1, retries + 1):
            try:
                conn = http.client.HTTPSConnection(url.netloc, timeout=self.timeout_seconds) if is_https else http.client.HTTPConnection(url.netloc, timeout=self.timeout_seconds)
                payload = json.dumps(body)
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                conn.request("POST", url.path, body=payload, headers=headers)
                resp = conn.getresponse()
                data = resp.read()
                if resp.status != 200:
                    raise RuntimeError(f"Kimi API HTTP {resp.status}: {data.decode('utf-8', 'ignore')}")
                parsed = json.loads(data.decode("utf-8"))
                # Prefer legacy DashScope-style format: output[0].content[0].text
                output = parsed.get("output")
                if isinstance(output, list) and output and isinstance(output[0], dict):
                    content_list = output[0].get("content")
                    if isinstance(content_list, list) and content_list and isinstance(content_list[0], dict):
                        text = content_list[0].get("text")
                        if isinstance(text, str):
                            return text
                # Fallback: OpenAI-compatible format: choices[0].message.content
                choices = parsed.get("choices")
                if isinstance(choices, list) and choices and isinstance(choices[0], dict):
                    message = choices[0].get("message", {})
                    text2 = message.get("content")
                    if isinstance(text2, str):
                        return text2
                raise RuntimeError(f"Unexpected Kimi response format: {parsed}")
            except Exception as e:
                if attempt == retries:
                    raise
                time.sleep(retry_delay_seconds)
        raise RuntimeError("Unreachable state in chat_completion.")


def load_kimi_client(config_path: str, model_override: Optional[str] = None) -> KimiClient:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # 支持模型覆盖，如果指定了 model_override 则使用它，否则使用配置文件中的模型
    # 如果配置文件中没有指定模型，则使用默认值
    model = model_override or cfg.get("model") or cfg.get("models", {}).get("default", "kimi-k2-thinking")
    return KimiClient(
        base_url=cfg.get("base_url", "https://api.moonshot.cn"),
        model=model,
        api_key_env=cfg.get("api_key_env", "KIMI_API_KEY"),
        default_temperature=cfg.get("default_temperature", 0.7),
        max_tokens=cfg.get("max_tokens", 4096),
        timeout_seconds=cfg.get("timeout", 60),
        endpoint_path=cfg.get("endpoint_path", "/v1/chat/completions"),
        request_format=cfg.get("request_format", "openai"),
    )


