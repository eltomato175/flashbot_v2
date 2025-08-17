# main.py
from __future__ import annotations
import asyncio
import logging
import sys
import os
from pathlib import Path

# Ensure UTF-8 on Windows consoles
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from utils.logger import setup_logger
from utils.config_loader import load_config
from utils.wallet_manager import WalletManager
from utils.failsafe import FailSafe
from strategies import (
    ArbitrageStrategy, MultiHopStrategy, MempoolStrategy,
    PriceLeakageStrategy, WhaleTrackingStrategy, CombinedStrategy
)

# Telegram imports (python-telegram-bot v20+)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

LOG = setup_logger("flashbot_main")

# --- Load config ---
CFG = load_config("config/settings.json")
TELEGRAM_TOKEN = CFG.get("telegram_token", "")
ADMIN_CHAT_ID = int(CFG.get("telegram_chat_id") or 0)
MIN_PROFIT = float(CFG.get("min_profit", 0.0))
FAILSAFE_CFG = CFG.get("failsafe", {})
MAX_LOSS = float(FAILSAFE_CFG.get("max_loss", -100.0))
MAX_VOLATILITY = float(FAILSAFE_CFG.get("max_volatility", 9999.0))

# --- Managers ---
wallet_manager = WalletManager()
# For demo we add a simple placeholder wallet identifier (replace with Wallet objects)
wallet_manager.add_wallet("wallet_main")

failsafe = FailSafe(max_loss=MAX_LOSS, max_volatility=MAX_VOLATILITY)

# --- Build strategies and CombinedStrategy ---
arbitrage = ArbitrageStrategy(enabled=True, flashloan=True, rafales=True)
multihop = MultiHopStrategy(enabled=True, flashloan=False, rafales=True)
mempool = MempoolStrategy(enabled=True, flashloan=True, rafales=False)
price_leak = PriceLeakageStrategy(enabled=True, flashloan=True, rafales=False)
whale = WhaleTrackingStrategy(enabled=True, flashloan=True, rafales=True)

combined = CombinedStrategy([arbitrage, multihop, mempool, price_leak, whale], min_profit=MIN_PROFIT)

# --- Telegram handlers ---
def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Resume trading", callback_data="resume")],
        [InlineKeyboardButton("⏸ Emergency stop", callback_data="emergency_stop")],
        [InlineKeyboardButton("🔁 Force restart", callback_data="force_restart")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ])

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "FlashBot v2 control panel\nAdmin commands available.",
        reply_markup=build_keyboard()
    )

async def btn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
        await query.edit_message_text("Unauthorized")
        return

    if data == "resume":
        failsafe.resume()
        await query.edit_message_text("✅ Trading resumed by admin")
    elif data == "emergency_stop":
        failsafe.pause("admin emergency_stop")
        await query.edit_message_text("⛔ Emergency stop executed")
    elif data == "force_restart":
        failsafe.request_restart_now()
        await query.edit_message_text("🔁 Restart requested (will be handled by supervisor if present)")
    elif data == "status":
        await query.edit_message_text(format_status())

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("Unauthorized")
        return
    await update.message.reply_text(format_status())

async def cmd_emergency_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("Unauthorized")
        return
    failsafe.pause("admin /emergency_stop")
    await update.message.reply_text("⛔ Emergency stop executed")

async def cmd_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("Unauthorized")
        return
    failsafe.resume()
    await update.message.reply_text("✅ Trading resumed")

async def cmd_force_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("Unauthorized")
        return
    failsafe.request_restart_now()
    await update.message.reply_text("🔁 Restart requested")

def format_status() -> str:
    st = failsafe.status()
    lines = [
        f"Paused: {st['paused']}",
        f"Accumulated profit (sum): {st['loss_accumulated']:.6f}",
        f"Max loss threshold: {st['max_loss']}",
        f"Max volatility threshold: {st['max_volatility']}",
        f"Reason: {st['reason'] or 'none'}",
        f"Request restart: {st['request_restart']}"
    ]
    return "\n".join(lines)

# --- Backend trade loop ---
async def trading_loop(app):
    LOG.info("Trading loop started")
    counter = 0
    while True:
        if failsafe.request_restart:
            LOG.warning("Restart requested by FailSafe. Exiting trading loop to allow supervisor restart.")
            # clean shutdown to let external supervisor restart (or we could os.exec)
            await app.bot.send_message(chat_id=ADMIN_CHAT_ID, text="🔁 Restarting as requested by admin/failsafe") if TELEGRAM_TOKEN and ADMIN_CHAT_ID else None
            # break to allow process supervisor to restart if present
            break

        if failsafe.paused:
            LOG.info("Trading paused by FailSafe. Sleeping...")
            await asyncio.sleep(2)
            continue

        counter += 1
        LOG.info(f"Heartbeat {counter} - evaluating combined strategy")
        try:
            market_data = {}  # TODO: inject real market data
            # Evaluate -> simulate -> execute inside combined
            if combined.evaluate(market_data):
                best_wallet = wallet_manager.get_best_wallet()
                combined.execute(best_wallet)
                # After execution we expect strategies to call FailSafe.record_profit(...)
                # For demo, we simulate a profit reading from CombinedStrategy execution by scanning logs or returning value.
                # Here, no profit returned by execute; in real code each strategy.execute should return profit
            else:
                LOG.info("No simulated profitable strategy this cycle")
        except Exception as e:
            LOG.exception(f"Error in trading loop: {e}")
            # On unexpected exception, pause trading
            failsafe.pause(f"exception: {e}")

        await asyncio.sleep(5)  # main heartbeat

    LOG.info("Trading loop ended")

# --- Application start ---
async def main_async():
    LOG.info("Starting FlashBot main async")
    app = None
    if TELEGRAM_TOKEN:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start_cmd))
        app.add_handler(CommandHandler("status", cmd_status))
        app.add_handler(CommandHandler("emergency_stop", cmd_emergency_stop))
        app.add_handler(CommandHandler("resume", cmd_resume))
        app.add_handler(CommandHandler("force_restart", cmd_force_restart))
        app.add_handler(CallbackQueryHandler(btn_callback))
        await app.initialize()
        await app.start()
        LOG.info("Telegram bot started")

    # Run trading loop in parallel with Telegram (if present)
    if app:
        await asyncio.gather(app.updater.start_polling(), trading_loop(app))
    else:
        # No Telegram, just run the trading loop with a dummy app object with .bot methods
        class DummyBot:
            async def send_message(self, chat_id, text):
                LOG.info(f"DummyBot would send to {chat_id}: {text}")
        class DummyApp:
            bot = DummyBot()
        await trading_loop(DummyApp())

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        LOG.info("Exiting on KeyboardInterrupt")
