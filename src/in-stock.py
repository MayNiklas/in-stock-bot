import os
from typing import List
import atexit
import datetime
import logging
from random import randint
from time import sleep

import requests
import telegram
from fake_headers import Headers
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

import csv_utils

# get environment variables
LINK = os.environ["LINK"]
apiKey = os.environ["API_Key"]

expected = int(os.environ["expected"])
unavailabilityMessage = os.environ["unavailabilityMessage"]

""" define global variables """
newProxyList = []


def startCommand(update: Update, context: CallbackContext) -> None:
    """ Telegram Command /start """
    chat_ids = update.message.chat_id
    update.message.reply_text(
        f"Bot has started!\nYour message ID: {chat_ids}\nYou will receive notifications in the future!"
    )
    chat = writer.add(update.message.chat)


""" init Telegram-Bot """
bot = telegram.Bot(token=apiKey)

""" gets the read / write object """
writer = csv_utils.Writer()


@atexit.register
def goodbye():
    """ makes sure the list is written before shuting down """
    writer.write()
    print("Saved to file - stopping now")


""" init updater """
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
updater = Updater(apiKey, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", startCommand))
updater.start_polling()


def dispatch_update(writer: csv_utils.Writer, text: str) -> None:
    """ Iterates trough the list of chat objects - sending update """
    for chat in writer.entries:
        bot.send_message(chat_id=chat.id, text=text)


def progbar(count: int, title: str) -> None:
    """ create a progress bar """
    for i in range(count):
        print(f"{i * '█'}{(count - 1 - i) * ' '} - {i + 1}/{count} {title}", end="\r")
        yield i


def make_request():
    """check the Availability of the Product, by looking if a specified 'unavailable' String is present fewer times then expected """
    """ generate random Windows Google Chrome fake header """
    chromedriverPath = "chromedriver"
    headers = Headers(browser="chrome", os="win", headers=True).generate()

    """ make a request for random product """
    req = requests.get(LINK)

    """ waiting for website response """
    for i in progbar(5, "waiting for Website response..."):
        sleep(1)

    """ work only with proxys wich has a fast response time """
    if req.status_code == 200:
        """ create Chrome configuration """
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("user-agent=" + headers["User-Agent"])
        chrome = webdriver.Chrome(executable_path=chromedriverPath, options=options)
        chrome.get(LINK)

        """ wait before page is loading """
        for i in progbar(10, "waiting for page loading is complete..."):
            sleep(1)

        """ check if UnavailableText is visible on the page """
        # searching for text block
        result: List[WebElement] = chrome.find_elements_by_link_text(
            unavailabilityMessage
        )
        chrome.quit()
        if len(result) != expected:
            return True
    return False


def check_site():
    """ check the Availability of the Product """
    while True:
        # checking if site changed expected state
        if make_request():
            sleep(5)
            # check if it really changed and didnt just encounter an error the first time
            if make_request():
                print(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Caught change!\n'
                )
                dispatch_update(
                    writer,
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                    f"\nState of your tracked Site has changed:\n {LINK}",
                )
        """ wait before make a new request for checking the product """
        sleep(randint(30, 40))


# calling make request function
check_site()
