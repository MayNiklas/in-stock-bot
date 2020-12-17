import atexit
import datetime
import logging
import os
from random import randint
from time import sleep

import telegram
from fake_headers import Headers
from selenium import webdriver
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

import csv_utils

# get Configuration from docker-compose.yml file
apiKey = os.environ['API_Key']
product = os.environ['Product']
productUrl = os.environ['Product_URL']
unavailabilityMessage = os.environ['UnavailableText']

# define global variables
chromedriverPath = 'chromedriver'
availability = False

# Telegram Command /start
def startCommand(update: Update, context: CallbackContext) -> None:
    chat_ids = update.message.chat_id
    update.message.reply_text(f"Bot has started!\nYour message ID: {chat_ids}\nYou will receive notifications in the future!")
    chat = writer.add(update.message.chat)

# init Telegram-Bot
bot = telegram.Bot(token=apiKey)

# gets the read / write object
writer = csv_utils.Writer()

# makes sure the list is written before shuting down
@atexit.register
def goodbye():
    writer.write()
    print("Saved to file - stopping now")

# init updater
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
updater = Updater(apiKey, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", startCommand))
updater.start_polling()

def dispatch_update(writer: object, text: str) -> None:
    # Iterates trough the list of chat objects - sending update
    for chat in writer.entries:
        bot.send_message(chat_id=chat.id, text=text)
        
# check the Availability of the Product
while availability == False:

    # generade random Windows Google Chrome fake header
	headers = Headers(
		browser="chrome",
		os="win",
		headers=True
	).generate()

	# create Selenium Chrome configuration
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("user-agent="+headers["User-Agent"])
	chrome = webdriver.Chrome(executable_path=chromedriverPath, options=options)
	chrome.get(productUrl)

	# check if UnavailableText is visible on the page
	if not chrome.find_elements_by_xpath("//*[contains(text(),'"+unavailabilityMessage+"')]"):
		dispatch_update(writer, text=f'Jetzt {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ist das {product} lieferbar! \n {productUrl}')
		dispatch_update(writer, text=f'Falls du das {product} weiterhin hier {productUrl} beobachten willst, musst du den Docker Container neu starten.')
		availability = True
		chrome.quit()

	# wait before make a new request for checking the product
	sleep(randint(30,60))

updater.idle()
