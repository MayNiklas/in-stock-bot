import time
import logging
import telegram
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_Key = '<API_Key>'
chat_id = '<chat_id>'
Product = '<Product'
Product_URL = '<URL>'

### You won't receive notifications by using /start at this point!
### Feature is in work!
def notify(update: Update, context: CallbackContext) -> None:
	chat_ids = update.message.chat_id
	update.message.reply_text(f"Bot has started!\nYour message ID: {chat_ids}\nYou will receive notifications in the future!")

# init telegram
bot = telegram.Bot(token=API_Key)

# init updater
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
updater = Updater(API_Key, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", notify))
updater.start_polling()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

while True:
	response = requests.get(f'{Product_URL}', headers=headers)
	print(response.text)
	if not '<span style="color:red;font-size:12px;font-weight:bold;">Leider ist dieser Artikel nicht mehr verf&uuml;gbar.</span>' in response.text:
		bot.send_message(chat_id=chat_id,text=f'{Product} lieferbar! {Product_URL}')
	time.sleep(60)

updater.idle()
driver.close()
