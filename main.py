import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8763987035:AAG-LvIXsUoY_kZpaZlI0ESNjISTG5PsgLs"

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot OK")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lien personnalisé vers ton profil Tondebruno
    support_link = 'https://t.me/Tondebruno'
    
    keyboard = [
        [InlineKeyboardButton("🛒 Acheter un VPN", callback_data='buy_vpn')],
        [InlineKeyboardButton("💼 Espace Revendeur", callback_data='reseller')],
        [InlineKeyboardButton("📢 Canal Officiel", url='https://t.me/+wZ6VGTvjTR44Y2E8')],
        [InlineKeyboardButton("👨‍💻 Support Client", url='https://t.me/Tondebruno')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = "👋 **Bienvenue sur VPN Pro Bot !**\n\nChoisissez une option :"
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'buy_vpn':
        await query.message.reply_text("💳 Contactez @Tondebruno pour les offres.")
    elif query.data == 'reseller':
        await query.message.reply_text("💼 Contactez @Tondebruno pour devenir revendeur.")

def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
