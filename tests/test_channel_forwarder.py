from pathlib import Path

from app.bot.channel_forwarder import (
    FILTER_TEXT_DEFAULT,
    extract_message_text,
    has_string_session,
    load_forwarded_ids,
    load_forwarder_settings,
    match_message,
    save_forwarded_ids,
    should_forward,
)


def test_extract_message_text_prefers_message_body() -> None:
    assert extract_message_text("본문", "캡션") == "본문"


def test_extract_message_text_falls_back_to_caption() -> None:
    assert extract_message_text(None, "캡션") == "캡션"


def test_match_message_finds_filter_text() -> None:
    result = match_message(f"종목 공시\n{FILTER_TEXT_DEFAULT}\n추가 문장", FILTER_TEXT_DEFAULT)
    assert result.matched is True


def test_match_message_returns_false_when_filter_missing() -> None:
    result = match_message("다른 내용", FILTER_TEXT_DEFAULT)
    assert result.matched is False


def test_forwarded_ids_round_trip(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    save_forwarded_ids(str(state_path), {10, 2})
    assert load_forwarded_ids(str(state_path)) == {2, 10}


def test_should_forward_skips_duplicates() -> None:
    assert should_forward(101, {99, 100}) is True
    assert should_forward(100, {99, 100}) is False


def test_has_string_session_detects_non_empty_value(monkeypatch) -> None:
    monkeypatch.setenv("TELEGRAM_STRING_SESSION", "abc123")
    settings = load_forwarder_settings()
    assert has_string_session(settings) is True
