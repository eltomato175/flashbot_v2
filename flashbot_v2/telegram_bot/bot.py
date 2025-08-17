from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

class FlashBotTelegram:
    def __init__(self, token, combined_strategy):
        self.token = token
        self.combined_strategy = combined_strategy
        self.app = Application.builder().token(token).build()

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.handle_buttons))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("Exécuter stratégies", callback_data="run")],
            [InlineKeyboardButton("Afficher config", callback_data="config")],
            [InlineKeyboardButton("Stop", callback_data="stop")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Bienvenue sur FlashBot 🚀", reply_markup=reply_markup)

    async def handle_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "run":
            results = self.combined_strategy.execute({"prices": [100, 102, 101, 105]})
            await query.edit_message_text(text=f"Résultats: {results}")

        elif query.data == "config":
            await query.edit_message_text(text="Config: min_profit, rafale, flashloan…")

        elif query.data == "stop":
            await query.edit_message_text(text="Bot stoppé.")
            await self.app.shutdown()

    def run(self):
        self.app.run_polling()
