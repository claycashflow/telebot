from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


FILTER_TEXT_DEFAULT = "보유목적 : 단순투자"
SOURCE_CHANNEL_DEFAULT = "darthacking"
TARGET_CHANNEL_DEFAULT = "justinvestcheck"
STATE_PATH_DEFAULT = "forwarder_state.json"


@dataclass(frozen=True)
class ForwarderSettings:
    api_id: str = ""
    api_hash: str = ""
    phone: str = ""
    login_code: str = ""
    password: str = ""
    string_session: str = ""
    session_name: str = "telebot_forwarder"
    source_channel: str = SOURCE_CHANNEL_DEFAULT
    target_channel: str = TARGET_CHANNEL_DEFAULT
    filter_text: str = FILTER_TEXT_DEFAULT
    state_path: str = STATE_PATH_DEFAULT


@dataclass(frozen=True)
class MatchResult:
    matched: bool
    text: str


def load_forwarder_settings() -> ForwarderSettings:
    load_dotenv()
    return ForwarderSettings(
        api_id=os.getenv("TELEGRAM_API_ID", ""),
        api_hash=os.getenv("TELEGRAM_API_HASH", ""),
        phone=os.getenv("TELEGRAM_PHONE", ""),
        login_code=os.getenv("TELEGRAM_LOGIN_CODE", ""),
        password=os.getenv("TELEGRAM_2FA_PASSWORD", ""),
        string_session=os.getenv("TELEGRAM_STRING_SESSION", ""),
        session_name=os.getenv("TELEGRAM_SESSION_NAME", "telebot_forwarder"),
        source_channel=os.getenv("TELEGRAM_SOURCE_CHANNEL", SOURCE_CHANNEL_DEFAULT),
        target_channel=os.getenv("TELEGRAM_TARGET_CHANNEL", TARGET_CHANNEL_DEFAULT),
        filter_text=os.getenv("TELEGRAM_FILTER_TEXT", FILTER_TEXT_DEFAULT),
        state_path=os.getenv("TELEGRAM_FORWARDER_STATE_PATH", STATE_PATH_DEFAULT),
    )


def extract_message_text(message_text: str | None, caption_text: str | None = None) -> str:
    return (message_text or caption_text or "").strip()


def match_message(message_text: str | None, filter_text: str, caption_text: str | None = None) -> MatchResult:
    text = extract_message_text(message_text=message_text, caption_text=caption_text)
    return MatchResult(matched=filter_text in text, text=text)


def validate_forwarder_settings(settings: ForwarderSettings) -> list[str]:
    missing = []
    if not settings.api_id:
        missing.append("TELEGRAM_API_ID")
    if not settings.api_hash:
        missing.append("TELEGRAM_API_HASH")
    if not settings.phone and not has_string_session(settings):
        missing.append("TELEGRAM_PHONE")
    return missing


def load_forwarded_ids(state_path: str) -> set[int]:
    path = Path(state_path)
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    forwarded_ids = data.get("forwarded_message_ids", [])
    return {int(message_id) for message_id in forwarded_ids}


def save_forwarded_ids(state_path: str, forwarded_ids: set[int]) -> None:
    path = Path(state_path)
    payload = {"forwarded_message_ids": sorted(forwarded_ids)}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def should_forward(message_id: int, forwarded_ids: set[int]) -> bool:
    return message_id not in forwarded_ids


def has_string_session(settings: ForwarderSettings) -> bool:
    return bool(settings.string_session.strip())
