from telegram.ext import Application, CommandHandler

from app.bot.handlers import check_handler, help_handler, start_handler
from app.config.settings import Settings


def build_bot_application(settings: Settings) -> Application:
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["settings"] = settings
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("check", check_handler))
    return application
