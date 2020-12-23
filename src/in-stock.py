import atexit
import datetime
import logging
import json
from random import randint
from time import sleep

import requests
import telegram
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from selenium import webdriver
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

import csv_utils


''' get Configuration from config.json file '''
with open('/app/data/config.json') as json_file:
    data = json.load(json_file)
    apiKey = data["telegram"]

''' define global variables '''
chromedriverPath = 'chromedriver'
newProxyList = []

''' Telegram Command /start '''
def startCommand(update: Update, context: CallbackContext) -> None:
    chat_ids = update.message.chat_id
    update.message.reply_text(
        f"Bot has started!\nYour message ID: {chat_ids}\nYou will receive notifications in the future!")
    chat = writer.add(update.message.chat)


''' init Telegram-Bot '''
bot = telegram.Bot(token=apiKey)

''' gets the read / write object '''
writer = csv_utils.Writer()

''' makes sure the list is written before shuting down '''

@atexit.register
def goodbye():
    writer.write()
    print("Saved to file - stopping now")

''' init updater '''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
updater = Updater(apiKey, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", startCommand))
updater.start_polling()

def dispatch_update(writer: object, text: str) -> None:
    ''' Iterates trough the list of chat objects - sending update '''
    for chat in writer.entries:
        bot.send_message(chat_id=chat.id, text=text)

''' create a progress bar '''
def progbar(count: int, title: str) -> None:
    for i in range(count):
        print(f"{i*'█'}{(count-1-i)*' '} - {i+1}/{count} {title}", end="\r")
        yield i

''' check the Availability of the Product '''
while True:
    ''' generade random Windows Google Chrome fake header '''
    headers = Headers(browser="chrome", os="win", headers=True).generate()

    ''' coise random product '''
    randomProduct = randint(0, len(data["product"])-1)
    productName = data["product"][randomProduct]["name"]
    productUrl = data["product"][randomProduct]["url"]
    unavailabilityMessage = data["product"][randomProduct]["value"]

    ''' make a request for random product '''
    req = requests.get(productUrl)

    ''' waiting for website response '''
    for i in progbar(5, "waiting for Website response..."):
        sleep(1)
     
    ''' work only with proxys wich has a fast response time '''
    if req.status_code == 200:
        ''' create Chrome configuration '''
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("user-agent="+headers["User-Agent"])
        chrome = webdriver.Chrome(
            executable_path=chromedriverPath, options=options)
        chrome.get(productUrl)

        ''' wait before page is loading '''
        for i in progbar(10, "waiting for page loading is complete..."):
            sleep(1)

        ''' check if UnavailableText is visible on the page '''
        searchMessage = chrome.find_elements_by_xpath(
            "//*[contains(text(),'"+unavailabilityMessage+"')]")
        if len(searchMessage) != 0:
            dispatch_update(
                writer, text=f'Jetzt {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ist das {productName} lieferbar! \n {productUrl}')
            chrome.quit()

        ''' wait before make a new request for checking the product '''
        sleep(randint(30, 40))

updater.idle()
