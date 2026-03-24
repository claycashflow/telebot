import json

from telegram import Update
from telegram.ext import ContextTypes

from app.application.sample_payload import SAMPLE_PAYLOAD
from app.application.service import run_market_check
from app.domain.validator import ValidationError


USAGE_TEXT = (
    "사용 방법\n"
    "1. JSON 데이터를 그대로 보내고\n"
    "2. 그 메시지에 답장한 뒤 /check 를 입력하거나\n"
    "3. /check { ... } 형태로 JSON을 같이 보낸다.\n\n"
    "빠른 테스트용으로 /check sample 도 사용할 수 있다."
)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "시장 저점 판독 봇이다.\n"
        "수동 입력 JSON을 받아 규칙 기반으로 판정한다.\n\n"
        f"{USAGE_TEXT}"
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(USAGE_TEXT)


async def check_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    try:
        payload = _extract_payload(update, context)
        _, _, report = run_market_check(payload)
        await update.message.reply_text(report)
    except ValidationError as exc:
        await update.message.reply_text(f"입력 검증 오류: {exc}")
    except ValueError as exc:
        await update.message.reply_text(f"입력 파싱 오류: {exc}\n\n{USAGE_TEXT}")
    except Exception as exc:  # noqa: BLE001
        await update.message.reply_text(f"처리 중 오류가 발생했다: {exc}")


def _extract_payload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> dict:
    if context.args and len(context.args) == 1 and context.args[0].lower() == "sample":
        return SAMPLE_PAYLOAD.copy()

    text_from_args = " ".join(context.args).strip()
    if text_from_args:
        return _load_json(text_from_args)

    reply = update.message.reply_to_message if update.message else None
    if reply and reply.text:
        return _load_json(reply.text)

    raise ValueError("JSON 입력이 필요하다.")


def _load_json(raw_text: str) -> dict:
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError("유효한 JSON 형식이 아니다.") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON 최상위 구조는 객체여야 한다.")
    return payload
