#!/usr/bin/env python3
"""Minimal Doubao / Volcengine Ark chat-completions provider.

Uses only Python stdlib so the runner works before users install any SDK.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional


DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"


class ArkProviderError(RuntimeError):
    """Raised when Ark returns an API or transport error."""


@dataclass
class ChatResult:
    content: str
    raw: dict[str, Any]
    usage: dict[str, Any]
    model: str
    latency_s: float


class DoubaoArkProvider:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout_s: int = 180,
    ) -> None:
        self.api_key = api_key or os.getenv("ARK_API_KEY", "")
        self.base_url = (base_url or os.getenv("ARK_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout_s = timeout_s
        if not self.api_key:
            raise ArkProviderError("Missing ARK_API_KEY. Put it in .env or export it in your shell.")

    def chat(
        self,
        *,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
    ) -> ChatResult:
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        started = time.time()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ArkProviderError(f"Ark HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ArkProviderError(f"Ark transport error: {exc.reason}") from exc

        latency_s = time.time() - started
        try:
            raw = json.loads(body)
            content = raw["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise ArkProviderError(f"Unexpected Ark response: {body[:1000]}") from exc

        return ChatResult(
            content=content,
            raw=raw,
            usage=raw.get("usage", {}),
            model=model,
            latency_s=latency_s,
        )
