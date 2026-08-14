from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

MAX_HISTORY_EXCHANGES = 5


@dataclass
class ConversationExchange:
    user_message: str
    assistant_message: str
    generated_sql: Optional[str] = None


class ConversationMemory:
    """Simple in-memory conversation history for follow-up context."""

    def __init__(self, max_exchanges: int = MAX_HISTORY_EXCHANGES) -> None:
        self.max_exchanges = max_exchanges
        self._history: List[ConversationExchange] = []

    def add_user_message(self, user_message: str) -> None:
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty.")

        self._history.append(ConversationExchange(user_message=user_message.strip(), assistant_message=""))
        self._trim_history()

    def add_assistant_message(self, assistant_message: str, generated_sql: Optional[str] = None) -> None:
        if not self._history:
            raise ValueError("No user message available to attach assistant response to.")

        if not assistant_message or not assistant_message.strip():
            raise ValueError("Assistant message cannot be empty.")

        exchange = self._history[-1]
        exchange.assistant_message = assistant_message.strip()
        if generated_sql:
            exchange.generated_sql = generated_sql.strip()

    def add_exchange(self, user_message: str, assistant_message: str, generated_sql: Optional[str] = None) -> None:
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty.")
        if not assistant_message or not assistant_message.strip():
            raise ValueError("Assistant message cannot be empty.")

        self._history.append(
            ConversationExchange(
                user_message=user_message.strip(),
                assistant_message=assistant_message.strip(),
                generated_sql=generated_sql.strip() if generated_sql else None,
            )
        )
        self._trim_history()

    def _trim_history(self) -> None:
        if len(self._history) > self.max_exchanges:
            self._history = self._history[-self.max_exchanges :]

    def get_recent_exchanges(self) -> List[ConversationExchange]:
        return list(self._history)

    def get_recent_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        for exchange in self._history:
            messages.append({"role": "user", "content": exchange.user_message})
            assistant_content = exchange.assistant_message
            if exchange.generated_sql:
                assistant_content = f"{assistant_content}\n\nGenerated SQL:\n{exchange.generated_sql}"
            messages.append({"role": "assistant", "content": assistant_content})
        return messages

    def clear(self) -> None:
        self._history.clear()


memory = ConversationMemory()
