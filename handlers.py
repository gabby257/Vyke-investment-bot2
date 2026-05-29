from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from db import cursor, conn

ADMIN_ID = 7593435783

PLANS = {
    "Starter": 3000,
    "Premium": 18000,
    "VIP": 108000
}

def menu():
    return ReplyKeyboardMarkup(
        [["💰 Deposit", "📈 Invest"], ["💳 Balance", "📊 Dashboard"]],
        resize_keyboard=True
    )

async def start(update, context):
    uid = update.effective_user.id

    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (uid,))
    cursor.execute("INSERT OR IGNORE INTO balances(user_id, amount) VALUES(?,0)", (uid,))
    conn.commit()

    await update.message.reply_text("🚀 Welcome to Vyke Bot", reply_markup=menu())

async def buttons(update, context):
    text = update.message.text
    uid = update.effective_user.id

    # 💰 DEPOSIT
    if text == "💰 Deposit":
        await update.message.reply_text(
            "💰 DEPOSIT DETAILS\n\n"
            "🏦 Bank Name: PALMPAY\n"
            "💳 Account Number: 9138224769\n"
            "👤 Account Name: WISDOM ABEL\n\n"
            "Send proof after payment for approval."
        )

    # 💳 BALANCE
    elif text == "💳 Balance":
        bal = cursor.execute("SELECT amount FROM balances WHERE user_id=?", (uid,)).fetchone()
        await update.message.reply_text(f"💰 Balance: ₦{bal[0] if bal else 0}")

    # 📈 INVEST
    elif text == "📈 Invest":
        kb = [
            [InlineKeyboardButton(f"{k} - ₦{v}", callback_data=f"inv_{k}")]
            for k, v in PLANS.items()
        ]
        await update.message.reply_text("Choose plan:", reply_markup=InlineKeyboardMarkup(kb))

    # 📊 DASHBOARD
    elif text == "📊 Dashboard":
        bal = cursor.execute("SELECT amount FROM balances WHERE user_id=?", (uid,)).fetchone()
        await update.message.reply_text(
            f"📊 DASHBOARD\n\n💰 Balance: ₦{bal[0] if bal else 0}"
        )
