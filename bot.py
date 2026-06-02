from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from wakeonlan import send_magic_packet
import os
import requests
import platform
import subprocess

# =====================
TOKEN = os.getenv("TOKEN")
OWNER_ID = 1460740609

PC_MAC = "A8:A1:59:E8:9A:7D"
PC_IP = "192.168.0.103"
# =====================


def is_owner(user_id: int):
    return user_id == OWNER_ID


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Включить ПК", callback_data="on")],
        [InlineKeyboardButton("🎮 Dota 2", callback_data="dota")],
        [InlineKeyboardButton("📡 Статус ПК", callback_data="status")],
        [InlineKeyboardButton("🔴 Выключить ПК", callback_data="off")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Доступ запрещён")
        return

    await update.message.reply_text("⚙️ Railway PC Control", reply_markup=menu())


# =====================
# ОТПРАВКА КОМАНД НА ПК ЧЕРЕЗ TELEGRAM
# =====================
def send_command(text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={
        "chat_id": OWNER_ID,
        "text": text
    })


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not is_owner(query.from_user.id):
        await query.answer("Нет доступа", show_alert=True)
        return

    await query.answer()

    # 🟢 ВКЛ ПК
    if query.data == "on":
        send_magic_packet(PC_MAC)
        await query.message.reply_text("🟢 Сигнал на включение отправлен")

    # 🎮 DOTA
    elif query.data == "dota":
        send_command("/dota")
        await query.message.reply_text("🎮 Запускаю Dota на ПК")

    # 📡 СТАТУС (простой вариант — позже улучшим агентом)
    elif query.data == "status":
        await query.message.reply_text("📡 Статус проверяет агент на ПК")

    # 🔴 ВЫКЛ ПК
    elif query.data == "off":
        send_command("/shutdown")
        await query.message.reply_text("🔴 Выключаю ПК")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🤖 BOT RUNNING (RAILWAY)")
app.run_polling()