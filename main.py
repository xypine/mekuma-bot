import logging
import os
from dotenv import load_dotenv
import requests


load_dotenv()


from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.warning(f"Got message from {update.effective_chat.username}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Kirjoita botille /makkara"
    )


async def makkara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api_url = "https://makkara.fly.dev/api"
    response = requests.get(api_url)
    data = response.json()

    message = f"Meksikolaista uunimakkaraa on saatavilla näistä ravintoloista: {data}"

    logging.warning(f"Got message from {update.effective_chat.username}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


print("RUNNING")
application = ApplicationBuilder().token(TOKEN).build()

start_handler = CommandHandler("start", start)
makkara_handler = CommandHandler("makkara", makkara)
application.add_handler(start_handler)
application.add_handler(makkara_handler)

application.run_polling()
