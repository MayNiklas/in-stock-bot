from unittest.mock import MagicMock

import app

ENV = {
    "LINK": "https://example.test/p",
    "API_Key": "123:TEST",
    "expected": "4",
    "unavailabilityMessage": "Nicht verfügbar",
}


def test_goodbye_saves_and_prints(capsys):
    notifier = MagicMock()

    app.goodbye(notifier)

    notifier.save.assert_called_once()
    assert "Saved to file" in capsys.readouterr().out


def test_configure_logging_sets_info_level(monkeypatch):
    basic = MagicMock()
    monkeypatch.setattr(app.logging, "basicConfig", basic)

    app.configure_logging()

    assert basic.call_args.kwargs["level"] == app.logging.INFO


def test_main_wires_bot_polling_and_checker(monkeypatch):
    bot_cls = MagicMock()
    writer_cls = MagicMock()
    updater_cls = MagicMock()
    checker_cls = MagicMock()
    register = MagicMock()
    monkeypatch.setattr(app.telegram, "Bot", bot_cls)
    monkeypatch.setattr(app.csv_utils, "Writer", writer_cls)
    monkeypatch.setattr(app, "Updater", updater_cls)
    monkeypatch.setattr(app, "StockChecker", checker_cls)
    monkeypatch.setattr(app.atexit, "register", register)
    monkeypatch.setattr(app, "configure_logging", MagicMock())

    app.main(ENV)

    bot_cls.assert_called_once_with(token="123:TEST")
    updater = updater_cls.return_value
    updater_cls.assert_called_once_with("123:TEST", use_context=True)
    updater.dispatcher.add_handler.assert_called_once()
    updater.start_polling.assert_called_once()
    register.assert_called_once()
    assert register.call_args[0][0] is app.goodbye

    kwargs = checker_cls.call_args.kwargs
    assert checker_cls.call_args.args[0].link == "https://example.test/p"
    assert kwargs["open_page"] is app.browser.open_page
    assert kwargs["make_user_agent"] is app.browser.make_user_agent
    checker_cls.return_value.run_forever.assert_called_once()
    updater.idle.assert_called_once()
