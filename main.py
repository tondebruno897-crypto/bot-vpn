import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token de ton bot Telegram
TOKEN = "8763987035:AAG-LvIXsUoY_kZpaZlI0ESNjISTG5PsgLs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Acheter un VPN", callback_data='buy_vpn')],
        [InlineKeyboardButton("💼 Espace Revendeur", callback_data='reseller')],
        [InlineKeyboardButton("📢 Canal Officiel", url='https://t.me/your_channel_link')],
        [InlineKeyboardButton("👨‍💻 Support Client", url='https://t.me/your_support_link')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = "👋 **Bienvenue sur VPN Pro Bot !**\n\nChoisissez une option dans le menu ci-dessous :"
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'buy_vpn':
        await query.message.reply_text("💳 Pour acheter un accès VPN, contactez directement le support ou choisissez une offre.")
    elif query.data == 'reseller':
        await query.message.reply_text("💼 Pour devenir revendeur, veuillez contacter l'administrateur.")

def main():
    # Configuration du bot avec la nouvelle version de python-telegram-bot
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Lancement du polling
    print("Bot démarré avec succès !")
    application.run_polling()

if __name__ == '__main__':
    main()
    
