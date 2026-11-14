"""Subscriber list and broadcast of notifications to Telegram chats."""
from typing import Callable


class Notifier:
    """Sends texts to every subscribed chat and persists the subscriber list."""

    def __init__(self, bot, writer):
        self.bot = bot
        self.writer = writer

    def broadcast(self, text: str) -> None:
        for chat in self.writer.entries:
            self.bot.send_message(chat_id=chat.id, text=text)

    def subscribe(self, chat):
        return self.writer.add(chat)

    def save(self) -> None:
        self.writer.write()


def make_start_handler(notifier: Notifier) -> Callable:
    """ creates the Telegram handler for /start """

    def start_command(update, context) -> None:
        chat_id = update.message.chat_id
        update.message.reply_text(
            f"Bot has started!\nYour message ID: {chat_id}\nYou will receive notifications in the future!")
        notifier.subscribe(update.message.chat)

    return start_command
