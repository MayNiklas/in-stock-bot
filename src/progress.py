"""Progress bar and timed waits used while polling the website."""
import time
from typing import Callable, Iterator


def progbar(count: int, title: str) -> Iterator[int]:
    """ create a progress bar """
    for i in range(count):
        print(f"{i * '█'}{(count - 1 - i) * ' '} - {i + 1}/{count} {title}", end="\r")
        yield i


def wait_with_progress(seconds: int, title: str, sleep: Callable[[float], None] = time.sleep) -> None:
    """ waits `seconds` seconds, one step per second, showing a progress bar """
    for _ in progbar(seconds, title):
        sleep(1)
