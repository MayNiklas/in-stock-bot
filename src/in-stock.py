import os
import time
import atexit
import logging
import telegram
import requests
from time import sleep
from random import randint
from telegram import Update
from fake_headers import Headers
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import csv_utils

API_Key = os.environ['API_Key']
Product = os.environ['Product']
Product_URL = os.environ['Product_URL']
UnavailableText = os.environ['UnavailableText']

### You won't receive notifications by using /start at this point!
### Feature is in work!
def notify(update: Update, context: CallbackContext) -> None:
    chat_ids = update.message.chat_id
    update.message.reply_text(f"Bot has started!\nYour message ID: {chat_ids}\nYou will receive notifications in the future!")
    chat = writer.add(update.message.chat)
    

# init telegram
bot = telegram.Bot(token=API_Key)

#gets the read / write object
writer = csv_utils.Writer()

#makes sure the list is written before shuting down
@atexit.register
def goodbye():
    writer.write()
    print("Saved to file - stopping now")

# init updater
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
updater = Updater(API_Key, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", notify))
updater.start_polling()

headers = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
).generate()


def dispatch_update(writer: object, text: str) -> None:
    """Iterates trough the list of chat objects - sending update"""
    for chat in writer.entries:
        bot.send_message(chat_id=chat.id, text=text)

while True:
    response = requests.get(f'{Product_URL}', headers=headers)
    if not UnavailableText in response.text:
       #sending update based on chat objects
       dispatch_update(writer, text=f'{Product} lieferbar! {Product_URL}')
    
    sleep(randint(30,60))

updater.idle()
driver.close()
