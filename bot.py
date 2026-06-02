from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = "8965348909:AAHFK4B5HyHZ9JHg4hhdLt-eQG36wXBZaBc"
OWNER_ID = 1460740609


def is_owner(user_id):
    return user_id == OWNER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update.effective_user.id):
        await update.message.reply_text("Доступ запрещён")
        return

    keyboard = [
        [InlineKeyboardButton("🎮 Запустить Dota 2", callback_data="dota")],
        [InlineKeyboardButton("🔴 Выключить ПК", callback_data="shutdown")]
    ]

    await update.message.reply_text(
        "Управление ПК",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if not is_owner(query.from_user.id):
        await query.answer("Нет доступа", show_alert=True)
        return

    await query.answer()

    if query.data == "dota":
        os.system('start steam://rungameid/570')
        await query.message.reply_text("Запускаю Dota 2")

    elif query.data == "shutdown":
        await query.message.reply_text("Выключаю ПК")
        os.system("shutdown /s /t 0")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен")

app.run_polling()