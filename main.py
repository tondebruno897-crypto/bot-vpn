import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Jeton officiel du bot Telegram
TOKEN = "8763987035:AAG-LvIXsUoY_kZpaZlI0ESNjISTG5PsgLs"

# Serveur web pour satisfaire la détection de port sur Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Le serveur du bot VPN est en cours d'exécution.".encode("utf-8"))

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Action au lancement : Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Acheter un VPN", callback_data='buy_vpn')],
        [InlineKeyboardButton("💼 Espace Revendeur", callback_data='reseller')],
        [InlineKeyboardButton("📢 Canal Officiel", url='https://t.me/your_channel_link')],
        [InlineKeyboardButton("👨‍💻 Support Client", url='https://t.me/your_support_link')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        "👋 **Bienvenue sur VPN Pro Bot !**\n\n"
        "Votre service de connexion sécurisée et rapide.\n"
        "Veuillez choisir une option dans le menu ci-dessous :"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# Gestion des clics sur les boutons du menu
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'buy_vpn':
        msg = (
            "💳 **Abonnement VPN**\n\n"
            "Pour souscrire à une offre ou obtenir un compte de test, "
            "veuillez contacter directement notre support client."
        )
        await query.message.reply_text(msg, parse_mode='Markdown')
    elif query.data == 'reseller':
        msg = (
            "💼 **Espace Revendeur**\n\n"
            "Vous souhaitez revendre nos accès VPN ? "
            "Contactez l'administrateur pour obtenir vos crédits et votre accès panneau."
        )
        await query.message.reply_text(msg, parse_mode='Markdown')

def main():
    # 1. Démarrage du serveur web de maintien de port en arrière-plan
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # 2. Initialisation du bot Telegram
    application = Application.builder().token(TOKEN).build()
    
    # 3. Ajout des commandes et événements
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot VPN lancé avec succès !")
    application.run_polling()

if __name__ == '__main__':
    main()
