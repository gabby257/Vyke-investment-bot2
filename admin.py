from db import cursor, conn
from telegram.ext import CommandHandler

ADMIN_ID = 7593435783

def register_admin_handlers(app):

    async def users(update, context):
        if update.effective_user.id != ADMIN_ID:
            return

        count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        await update.message.reply_text(f"👥 Users: {count}")

    async def broadcast(update, context):
        if update.effective_user.id != ADMIN_ID:
            return

        msg = " ".join(context.args)
        users = cursor.execute("SELECT user_id FROM users").fetchall()

        sent = 0
        for u in users:
            try:
                await context.bot.send_message(u[0], msg)
                sent += 1
            except:
                pass

        await update.message.reply_text(f"Broadcast sent to {sent} users")

    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("broadcast", broadcast))


async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("inv_"):
        plan = data.split("_")[1]
        await query.message.reply_text(f"Selected plan: {plan}")
