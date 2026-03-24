from app.application.sample_payload import SAMPLE_PAYLOAD
from app.application.service import run_market_check
from app.bot.app import build_bot_application
from app.bot.telegram_sender import TelegramSendError, send_text
from app.config.settings import load_settings


def main() -> None:
    settings = load_settings()
    if settings.telegram_bot_token:
        application = build_bot_application(settings.telegram_bot_token)
        print("Telegram bot polling started.")
        application.run_polling()
        return

    _, _, report = run_market_check(SAMPLE_PAYLOAD)
    print(report)
    if settings.telegram_bot_token and settings.telegram_chat_id:
        try:
            send_text(settings.telegram_bot_token, settings.telegram_chat_id, report)
            print("Telegram message sent.")
        except TelegramSendError as exc:
            print(f"Telegram send failed: {exc}")
    else:
        print("TELEGRAM_BOT_TOKEN is not set. Ran local sample mode instead.")


if __name__ == "__main__":
    main()
