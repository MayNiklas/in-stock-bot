"""Wiring: builds the Telegram bot, the subscriber list and the stock checker."""
import atexit
import logging
import time
import random

import requests
import telegram
from telegram.ext import CommandHandler, Updater

import browser
import csv_utils
from checker import StockChecker
from config import Settings
from notifier import Notifier, make_start_handler


def configure_logging() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )


def goodbye(notifier: Notifier) -> None:
    """ makes sure the list is written before shuting down """
    notifier.save()
    print("Saved to file - stopping now")


def main(env=None) -> None:
    settings = Settings.from_env(env)
    configure_logging()

    notifier = Notifier(telegram.Bot(token=settings.api_key), csv_utils.Writer())
    atexit.register(goodbye, notifier)

    updater = Updater(settings.api_key, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", make_start_handler(notifier)))
    updater.start_polling()

    checker = StockChecker(
        settings,
        http_get=requests.get,
        open_page=browser.open_page,
        make_user_agent=browser.make_user_agent,
        notify=notifier.broadcast,
        sleep=time.sleep,
        randint=random.randint,
    )
    checker.run_forever()
    updater.idle()
