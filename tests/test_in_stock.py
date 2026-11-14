import importlib
from unittest.mock import MagicMock

import pytest

in_stock = importlib.import_module("in-stock")


class Stop(Exception):
    """Raised by a patched sleep() to end the endless check loop."""


def stop_after(calls):
    """Return a sleep() replacement that raises Stop on the call after `calls` calls."""
    counter = {"n": 0}

    def fake_sleep(_seconds):
        counter["n"] += 1
        if counter["n"] > calls:
            raise Stop()

    return fake_sleep


@pytest.fixture
def fake_writer(monkeypatch):
    writer = MagicMock()
    writer.entries = []
    monkeypatch.setattr(in_stock, "writer", writer)
    return writer


@pytest.fixture
def fake_bot(monkeypatch):
    bot = MagicMock()
    monkeypatch.setattr(in_stock, "bot", bot)
    return bot


@pytest.fixture
def fake_requests(monkeypatch):
    requests_mock = MagicMock()
    monkeypatch.setattr(in_stock, "requests", requests_mock)
    return requests_mock


@pytest.fixture
def fake_chrome(monkeypatch):
    webdriver_mock = MagicMock()
    chrome = MagicMock()
    webdriver_mock.Chrome.return_value = chrome
    monkeypatch.setattr(in_stock, "webdriver", webdriver_mock)
    return chrome


@pytest.fixture
def no_sleep(monkeypatch):
    sleep_mock = MagicMock()
    monkeypatch.setattr(in_stock, "sleep", sleep_mock)
    monkeypatch.setattr(in_stock, "randint", MagicMock(return_value=45))
    return sleep_mock


def test_defaults_from_environment():
    assert in_stock.LINK == "https://example.test/product"
    assert in_stock.apiKey == "123:TEST"
    assert in_stock.expected == 4
    assert in_stock.unavailabilityMessage == "Nicht verfügbar"
    assert in_stock.min_interval == 30
    assert in_stock.max_interval == 90


def test_interval_read_from_environment(monkeypatch):
    monkeypatch.setenv("min_interval", "60")
    monkeypatch.setenv("max_interval", "120")
    try:
        reloaded = importlib.reload(in_stock)
        assert reloaded.min_interval == 60
        assert reloaded.max_interval == 120
    finally:
        monkeypatch.delenv("min_interval")
        monkeypatch.delenv("max_interval")
        importlib.reload(in_stock)


def test_start_command_replies_and_adds_chat(fake_writer):
    update = MagicMock()
    update.message.chat_id = 42

    in_stock.startCommand(update, MagicMock())

    update.message.reply_text.assert_called_once()
    assert "Your message ID: 42" in update.message.reply_text.call_args[0][0]
    fake_writer.add.assert_called_once_with(update.message.chat)


def test_goodbye_writes_file(fake_writer, capsys):
    in_stock.goodbye()

    fake_writer.write.assert_called_once()
    assert "Saved to file" in capsys.readouterr().out


def test_setup_creates_bot_writer_and_updater(monkeypatch):
    bot_cls = MagicMock()
    writer_cls = MagicMock()
    updater_cls = MagicMock()
    register = MagicMock()
    monkeypatch.setattr(in_stock.telegram, "Bot", bot_cls)
    monkeypatch.setattr(in_stock.csv_utils, "Writer", writer_cls)
    monkeypatch.setattr(in_stock, "Updater", updater_cls)
    monkeypatch.setattr(in_stock.atexit, "register", register)

    in_stock.setup()

    bot_cls.assert_called_once_with(token="123:TEST")
    writer_cls.assert_called_once_with()
    register.assert_called_once_with(in_stock.goodbye)
    updater_cls.assert_called_once_with("123:TEST", use_context=True)
    updater = updater_cls.return_value
    updater.dispatcher.add_handler.assert_called_once()
    updater.start_polling.assert_called_once()
    assert in_stock.updater is updater
    assert in_stock.writer is writer_cls.return_value
    assert in_stock.bot is bot_cls.return_value


def test_main_runs_setup_loop_and_idle(monkeypatch):
    setup = MagicMock()
    loop = MagicMock()
    monkeypatch.setattr(in_stock, "setup", setup)
    monkeypatch.setattr(in_stock, "make_request", loop)
    updater = MagicMock()
    monkeypatch.setattr(in_stock, "updater", updater)

    in_stock.main()

    setup.assert_called_once()
    loop.assert_called_once()
    updater.idle.assert_called_once()


def test_dispatch_update_sends_to_every_chat(fake_writer, fake_bot):
    fake_writer.entries = [MagicMock(id=1), MagicMock(id=2)]

    in_stock.dispatch_update(fake_writer, "hello")

    assert fake_bot.send_message.call_args_list == [
        ((), {"chat_id": 1, "text": "hello"}),
        ((), {"chat_id": 2, "text": "hello"}),
    ]


def test_dispatch_update_without_chats_sends_nothing(fake_writer, fake_bot):
    in_stock.dispatch_update(fake_writer, "hello")

    fake_bot.send_message.assert_not_called()


def test_progbar_yields_each_step(capsys):
    assert list(in_stock.progbar(3, "wait")) == [0, 1, 2]
    assert "3/3 wait" in capsys.readouterr().out


def test_make_request_non_200_skips_browser(fake_requests, fake_chrome, fake_writer, fake_bot, monkeypatch):
    fake_requests.get.return_value = MagicMock(status_code=503)
    monkeypatch.setattr(in_stock, "sleep", stop_after(5))

    with pytest.raises(Stop):
        in_stock.make_request()

    fake_requests.get.assert_called_with("https://example.test/product")
    fake_chrome.get.assert_not_called()
    fake_bot.send_message.assert_not_called()


def test_make_request_notifies_on_change(fake_requests, fake_chrome, fake_writer, fake_bot, no_sleep, monkeypatch):
    fake_requests.get.return_value = MagicMock(status_code=200)
    fake_chrome.find_elements_by_link_text.return_value = ["only one"]
    fake_writer.entries = [MagicMock(id=7)]
    monkeypatch.setattr(in_stock, "sleep", stop_after(100))

    with pytest.raises(Stop):
        in_stock.make_request()

    fake_chrome.get.assert_called_with("https://example.test/product")
    fake_chrome.find_elements_by_link_text.assert_called_with("Nicht verfügbar")
    fake_chrome.quit.assert_called()
    sent = fake_bot.send_message.call_args
    assert sent.kwargs["chat_id"] == 7
    assert "State of your tracked Site has changed" in sent.kwargs["text"]


def test_make_request_no_notification_when_state_matches(
        fake_requests, fake_chrome, fake_writer, fake_bot, monkeypatch):
    fake_requests.get.return_value = MagicMock(status_code=200)
    fake_chrome.find_elements_by_link_text.return_value = ["a", "b", "c", "d"]
    fake_writer.entries = [MagicMock(id=7)]
    monkeypatch.setattr(in_stock, "sleep", stop_after(100))
    monkeypatch.setattr(in_stock, "randint", MagicMock(return_value=1))

    with pytest.raises(Stop):
        in_stock.make_request()

    fake_bot.send_message.assert_not_called()
    fake_chrome.quit.assert_called()


def test_make_request_waits_random_interval_after_check(
        fake_requests, fake_chrome, fake_writer, monkeypatch):
    fake_requests.get.return_value = MagicMock(status_code=200)
    fake_chrome.find_elements_by_link_text.return_value = []
    randint_mock = MagicMock(return_value=45)
    monkeypatch.setattr(in_stock, "randint", randint_mock)
    sleep_mock = MagicMock(side_effect=[None] * 15 + [Stop()])
    monkeypatch.setattr(in_stock, "sleep", sleep_mock)

    with pytest.raises(Stop):
        in_stock.make_request()

    randint_mock.assert_called_with(in_stock.min_interval, in_stock.max_interval)
    assert sleep_mock.call_count == 16
