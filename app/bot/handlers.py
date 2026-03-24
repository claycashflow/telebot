import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from app.application.service import run_market_check
from app.domain.validator import ValidationError
from app.infrastructure.collector import collect_market_data


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "지금이뉘 - 저점인지 객관적으로 알아보기\n\n"
        "/check  : 현재 장 마감 데이터를 자동 수집해 저점 판독 결과를 보여준다.\n"
        "/help   : 도움말"
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "/check 를 입력하면 자동으로 데이터를 수집해 저점 판독 결과를 보낸다.\n"
        "데이터 수집에 30~60초 정도 소요될 수 있다."
    )


async def check_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    status_msg = await update.message.reply_text("데이터 수집 중... 잠시만 기다려주세요.")

    try:
        settings = context.application.bot_data.get("settings")
        fred_api_key = settings.fred_api_key if settings else ""

        loop = asyncio.get_event_loop()
        payload = await loop.run_in_executor(
            None, lambda: collect_market_data(fred_api_key)
        )

        _, _, report = run_market_check(payload)
        await status_msg.edit_text(report)

    except ValidationError as exc:
        await status_msg.edit_text(f"입력 검증 오류: {exc}")
    except Exception as exc:
        await status_msg.edit_text(f"데이터 수집 중 오류가 발생했다: {exc}")
