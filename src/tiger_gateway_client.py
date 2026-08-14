from __future__ import annotations

import requests
from requests import Response
from typing import Any, Dict, List

from .config import get_settings

DEFAULT_TIMEOUT_SECONDS = 15


class TigerGatewayError(Exception):
    """Raised when the configured LLM gateway cannot complete a request."""


class TigerGatewayClient:
    def __init__(self, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> None:
        settings = get_settings()
        self.gateway_url = settings.tiger_ai_gateway_url
        self.api_key = settings.tiger_ai_gateway_api_key
        self.model = settings.tiger_ai_gateway_model
        self.timeout = timeout

        if not self.gateway_url:
            raise TigerGatewayError("Missing required configuration: TIGER_AI_GATEWAY_URL.")
        if not self.api_key:
            raise TigerGatewayError("Missing required configuration: TIGER_AI_GATEWAY_API_KEY.")
        if not self.model:
            raise TigerGatewayError("Missing required configuration: TIGER_AI_GATEWAY_MODEL.")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )

    def _build_payload(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": messages,
        }

    def _raise_for_http_error(self, response: Response) -> None:
        if not response.ok:
            raise TigerGatewayError(
                f"LLM gateway request failed with status {response.status_code}: "
                f"{response.text.strip()[:500]}"
            )

    def _parse_response(self, response: Response) -> str:
        try:
            payload = response.json()
        except ValueError as exc:
            raise TigerGatewayError(f"Unable to parse JSON from LLM gateway response: {exc}")

        if not isinstance(payload, dict):
            raise TigerGatewayError("Unexpected LLM gateway response format: expected object.")

        if "error" in payload:
            error_value = payload["error"]
            raise TigerGatewayError(f"LLM gateway returned an error: {error_value}")

        if "choices" not in payload or not isinstance(payload["choices"], list) or not payload["choices"]:
            raise TigerGatewayError("LLM gateway response missing choices.")

        try:
            content = payload["choices"][0]["message"]["content"]
        except (KeyError, TypeError, IndexError) as exc:
            raise TigerGatewayError(
                f"Unable to extract assistant content from LLM gateway response: {exc}"
            )

        if not isinstance(content, str):
            raise TigerGatewayError("Assistant content is not text in LLM gateway response.")

        return content.strip()

    def send_chat(self, messages: List[Dict[str, str]]) -> str:
        if not messages:
            raise TigerGatewayError("Chat messages list cannot be empty.")

        payload = self._build_payload(messages)

        try:
            response = self.session.post(
                self.gateway_url,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise TigerGatewayError(f"Failed to send request to LLM gateway: {exc}")

        self._raise_for_http_error(response)
        return self._parse_response(response)
