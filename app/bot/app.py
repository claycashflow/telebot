from telegram.ext import Application, CommandHandler

from app.bot.handlers import check_handler, help_handler, start_handler


def build_bot_application(token: str) -> Application:
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("check", check_handler))
    return application
