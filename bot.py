from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from wakeonlan import send_magic_packet
import os
import platform
import subprocess
import time

# =====================
TOKEN = "8965348909:AAEicV6KS0pGQ_W-ciJXtuico6IqHMkS-io"
OWNER_ID = 1460740609

PC_MAC = "A8:A1:59:E8:9A:7D"  # ← вставь MAC своего ПК
# =====================


def is_owner(user_id: int):
    return user_id == OWNER_ID


def ping_pc():
    """
    Проверка доступности ПК
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "192.168.0.1"]  # ← ЗАМЕНИ НА IP ТВОЕГО ПК

    try:
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except:
        return False


def get_menu():
    keyboard = [
        [InlineKeyboardButton("🟢 Включить ПК", callback_data="on")],
        [InlineKeyboardButton("🎮 Запустить Dota 2", callback_data="dota")],
        [InlineKeyboardButton("📡 Статус ПК", callback_data="status")],
        [InlineKeyboardButton("🔴 Выключить ПК", callback_data="off")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Доступ запрещён")
        return

    await update.message.reply_text("⚙️ Панель управления ПК:", reply_markup=get_menu())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not is_owner(query.from_user.id):
        await query.answer("Нет доступа", show_alert=True)
        return

    await query.answer()

    # 🟢 ВКЛ ПК
    if query.data == "on":
        send_magic_packet(PC_MAC)
        await query.message.reply_text("🟢 Отправлен сигнал на включение ПК")

    # 🎮 DOTA
    elif query.data == "dota":
        os.system('start steam://rungameid/570')
        await query.message.reply_text("🎮 Запускаю Dota 2")

    # 📡 СТАТУС
    elif query.data == "status":
        if ping_pc():
            await query.message.reply_text("🟢 ПК онлайн")
        else:
            await query.message.reply_text("🔴 ПК оффлайн")

    # 🔴 ВЫКЛ
    elif query.data == "off":
        await query.message.reply_text("🔴 Выключаю ПК...")
        time.sleep(2)
        os.system("shutdown /s /t 0")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🤖 Бот запущен")
app.run_polling()