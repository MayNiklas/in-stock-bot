from unittest.mock import MagicMock

from notifier import Notifier, make_start_handler


def make_notifier(entries=()):
    writer = MagicMock()
    writer.entries = list(entries)
    bot = MagicMock()
    return Notifier(bot, writer), bot, writer


def test_broadcast_sends_to_every_chat():
    notifier, bot, _ = make_notifier([MagicMock(id=1), MagicMock(id=2)])

    notifier.broadcast("hello")

    assert bot.send_message.call_args_list == [
        ((), {"chat_id": 1, "text": "hello"}),
        ((), {"chat_id": 2, "text": "hello"}),
    ]


def test_broadcast_without_subscribers_sends_nothing():
    notifier, bot, _ = make_notifier()

    notifier.broadcast("hello")

    bot.send_message.assert_not_called()


def test_subscribe_adds_chat_to_writer():
    notifier, _, writer = make_notifier()
    chat = MagicMock()

    result = notifier.subscribe(chat)

    writer.add.assert_called_once_with(chat)
    assert result is writer.add.return_value


def test_save_writes_subscriber_list():
    notifier, _, writer = make_notifier()

    notifier.save()

    writer.write.assert_called_once()


def test_start_handler_replies_and_subscribes_chat():
    notifier = MagicMock()
    handler = make_start_handler(notifier)
    update = MagicMock()
    update.message.chat_id = 42

    handler(update, MagicMock())

    text = update.message.reply_text.call_args[0][0]
    assert "Your message ID: 42" in text
    notifier.subscribe.assert_called_once_with(update.message.chat)
