from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / ".env"
load_dotenv(DOTENV_PATH)


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Settings:
    mysql_host: str
    mysql_port: int
    mysql_database: str
    mysql_user: str
    mysql_password: str
    tiger_ai_gateway_url: str
    tiger_ai_gateway_api_key: str
    tiger_ai_gateway_model: str


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(
            f"Missing required environment variable: {name}."
            " Add it to your environment or .env file."
        )
    return value


def _get_int_env(name: str, default: int) -> int:
    raw = os.getenv(name, str(default))
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigError(f"Environment variable {name} must be an integer: {exc}")


def load_settings() -> Settings:
    return Settings(
        mysql_host=os.getenv("MYSQL_HOST", "localhost"),
        mysql_port=_get_int_env("MYSQL_PORT", 3306),
        mysql_database=_get_required_env("MYSQL_DATABASE"),
        mysql_user=_get_required_env("MYSQL_USER"),
        mysql_password=_get_required_env("MYSQL_PASSWORD"),
        tiger_ai_gateway_url=_get_required_env("TIGER_AI_GATEWAY_URL"),
        tiger_ai_gateway_api_key=_get_required_env("TIGER_AI_GATEWAY_API_KEY"),
        tiger_ai_gateway_model=_get_required_env("TIGER_AI_GATEWAY_MODEL"),
    )


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings
