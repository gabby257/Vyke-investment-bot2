import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from db import init_db
from handlers import start, buttons
from admin import register_admin_handlers, callback_handler

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7593435783

logging.basicConfig(level=logging.INFO)

print("🤖 Vyke Bot Starting...")

def main():
    if not TOKEN:
        raise Exception("TOKEN not set in Render environment variables")

    init_db()

    app = Application.builder().token(TOKEN).build()

    # User handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

    # Admin handlers
    register_admin_handlers(app)
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("Bot running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
