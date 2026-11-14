from unittest.mock import MagicMock

import browser


def test_make_user_agent_returns_chrome_agent(monkeypatch):
    headers_cls = MagicMock()
    headers_cls.return_value.generate.return_value = {"User-Agent": "Mozilla/5.0 test"}
    monkeypatch.setattr(browser, "Headers", headers_cls)

    assert browser.make_user_agent() == "Mozilla/5.0 test"
    headers_cls.assert_called_once_with(browser="chrome", os="win", headers=True)


def test_chrome_options_contain_all_arguments(monkeypatch):
    webdriver = MagicMock()
    monkeypatch.setattr(browser, "webdriver", webdriver)

    options = browser.chrome_options("ua-1")

    added = [c[0][0] for c in options.add_argument.call_args_list]
    assert added == browser.CHROME_ARGUMENTS + ["user-agent=ua-1"]
    assert options is webdriver.ChromeOptions.return_value


def test_open_page_starts_chrome_and_loads_link(monkeypatch):
    webdriver = MagicMock()
    monkeypatch.setattr(browser, "webdriver", webdriver)

    chrome = browser.open_page("https://example.test/p", "ua-2")

    webdriver.Chrome.assert_called_once_with(
        executable_path=browser.CHROMEDRIVER_PATH,
        options=webdriver.ChromeOptions.return_value,
    )
    chrome.get.assert_called_once_with("https://example.test/p")
    assert chrome is webdriver.Chrome.return_value
