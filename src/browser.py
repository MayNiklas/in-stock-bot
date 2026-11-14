"""Browser helpers: fake user agent and headless Chrome page loading."""
from fake_headers import Headers
from selenium import webdriver

CHROMEDRIVER_PATH = 'chromedriver'

CHROME_ARGUMENTS = [
    "--start-maximized",
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--ignore-certificate-errors",
]


def make_user_agent() -> str:
    """ random Windows Google Chrome user agent """
    return Headers(browser="chrome", os="win", headers=True).generate()["User-Agent"]


def chrome_options(user_agent: str):
    """ Chrome configuration for a headless session with the given user agent """
    options = webdriver.ChromeOptions()
    for argument in CHROME_ARGUMENTS:
        options.add_argument(argument)
    options.add_argument("user-agent=" + user_agent)
    return options


def open_page(link: str, user_agent: str):
    """ opens `link` in a new headless Chrome and returns the driver """
    chrome = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options(user_agent))
    chrome.get(link)
    return chrome
