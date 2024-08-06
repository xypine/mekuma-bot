import logging
import os
from dotenv import load_dotenv
import requests


load_dotenv()


from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder

TOKEN = os.getenv("TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.warning(f"Got message from {update.effective_chat.username}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Kirjoita botille /makkara"
    )


# /makkara command
async def makkara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Loading..."
    )
    api_url = "https://makkara.fly.dev/api"
    response = requests.get(api_url)
    data = response.json()
    data_list = []
    string = ""

    # check if there are multiple dates of sausages available
    multiple_days = False
    for i in data:
        if len(data[i]) > 1:
            multiple_days = True
            break

    # format result based on multiple_days
    if multiple_days == False:
        for i in data:
            data_list.append(str(f"{i}  -  {data[i][0]}"))
            string = "\n".join(data_list)
        message = f"Meksikolaista uunimakkaraa on saatavilla näistä ravintoloista: \n{string} \n\n\nTieto on suuntaa antavaa, varmista Unicafen sivuilta meksikolaisen uunimakkaran saatavuus."
    elif multiple_days == True:
        for i in data:
            data_list.append(str(f"{i} {data[i]}"))
        message = f"Meksikolaista uunimakkaraa on saatavilla näistä ravintoloista: {data_list}"

    logging.warning(f"Got message from {update.effective_chat.username}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


print("RUNNING")
application = ApplicationBuilder().token(TOKEN).build()

start_handler = CommandHandler("start", start)
makkara_handler = CommandHandler("makkara", makkara)
application.add_handler(start_handler)
application.add_handler(makkara_handler)

application.run_polling()
