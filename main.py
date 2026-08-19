import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Ton Token Telegram intégré
TOKEN = "8763987035:AAFVZzm0yPktps5u7km9S8OyowQf85tg6Nw"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name

    keyboard = [
        ["🛒 Acheter un VPN", "💼 Espace revendeur"],
        ["📁 Mes comptes"],
        ["📝 Fichier de test", "🔔 Notifications"],
        ["✉️ Message admin", "🤖 Assistance"],
        ["🎁 Gains & Parrainage"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, persistent=True
    )

    message = (
        f"✨ **BIENVENUE {user_name.upper()} !** ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 **VOTRE PROFIL**\n"
        f"🏷️ Nom : {user_name}\n"
        f"🆔 ID : `{update.effective_user.id}`\n\n"
        f"Que souhaitez-vous faire ?"
    )

    await update.message.reply_text(
        message, parse_mode="Markdown", reply_markup=reply_markup
    )


async def repondre_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = update.message.text

    if texte == "🛒 Acheter un VPN":
        keyboard_vpn = [
            ["🟠 Orange", "🔵 Moov"],
            ["🔙 Retour au menu"],
        ]
        await update.message.reply_text(
            "Choisissez votre réseau :",
            reply_markup=ReplyKeyboardMarkup(
                keyboard_vpn, resize_keyboard=True
            ),
        )
    elif texte == "📝 Fichier de test":
        await update.message.reply_text(
            "🥳 Obtenez votre fichier de test 24h gratuit !"
        )
    elif texte == "✉️ Message admin":
        await update.message.reply_text(
            "💌 Envoyez votre message à l'administrateur ici."
        )
    elif texte == "🔙 Retour au menu":
        await start(update, context)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, repondre_menu)
    )
    app.run_polling()
