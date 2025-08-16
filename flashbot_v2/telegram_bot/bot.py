from __future__ import annotations
import logging, asyncio
from typing import List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
log = logging.getLogger("TelegramBot")

def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🪙 Vérifier wallets", callback_data="check_wallets")],
        [InlineKeyboardButton("⚡ Exécuter meilleure stratégie", callback_data="run_best")],
        [InlineKeyboardButton("🎯 Rafales", callback_data="run_rafales")],
        [InlineKeyboardButton("ℹ️ Infos bot", callback_data="bot_info")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 FlashBot en ligne. Choisissez :", reply_markup=build_keyboard())

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE, *, api):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "check_wallets":
        msg = api.check_wallets_overview()
        await query.edit_message_text(msg)
    elif data == "run_best":
        res = api.run_best_strategy()
        await query.edit_message_text(f"✅ {res}")
    elif data == "run_rafales":
        res = api.run_rafales()
        await query.edit_message_text(f"✅ {res}")
    elif data == "bot_info":
        await query.edit_message_text(api.bot_info())

def build_app(token: str, api) -> "Application":
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(lambda u, c: callbacks(u, c, api=api)))
    return app
