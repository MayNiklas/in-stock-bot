"""Checks a product page for a change of its state and reports it."""
import datetime
from typing import Callable, Optional

from config import Settings
from progress import wait_with_progress

HTTP_OK = 200


def timestamp(now: Optional[datetime.datetime] = None) -> str:
    now = now or datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def is_changed(found: int, expected: int) -> bool:
    return found != expected


def change_message(link: str, now: Optional[datetime.datetime] = None) -> str:
    return f"{timestamp(now)}\nState of your tracked Site has changed:\n {link}"


class StockChecker:
    """
    All external parts are passed in, so the checker can be tested without
    network, browser or Telegram.
    """

    def __init__(self, settings: Settings, *, http_get: Callable, open_page: Callable,
                 make_user_agent: Callable[[], str], notify: Callable[[str], None],
                 sleep: Callable[[float], None], randint: Callable[[int, int], int]):
        self.settings = settings
        self.http_get = http_get
        self.open_page = open_page
        self.make_user_agent = make_user_agent
        self.notify = notify
        self.sleep = sleep
        self.randint = randint

    def check_once(self) -> Optional[bool]:
        """
        Runs one check. Returns None if the site did not answer with HTTP 200,
        otherwise whether the state changed.
        """
        link = self.settings.link
        response = self.http_get(link)
        wait_with_progress(5, "waiting for Website response...", self.sleep)
        if response.status_code != HTTP_OK:
            return None

        page = self.open_page(link, self.make_user_agent())
        wait_with_progress(10, "waiting for page loading is complete...", self.sleep)
        found = len(page.find_elements_by_link_text(self.settings.unavailability_message))

        changed = is_changed(found, self.settings.expected)
        if changed:
            print(f'{timestamp()} - Caught change!\n')
            self.notify(change_message(link))
        page.quit()
        return changed

    def run_forever(self) -> None:
        while True:
            if self.check_once() is not None:
                self.sleep(self.randint(self.settings.min_interval, self.settings.max_interval))
