import datetime
from unittest.mock import MagicMock

import pytest

from checker import StockChecker, change_message, is_changed, timestamp
from config import Settings


class Stop(Exception):
    """Raised by a patched sleep() to end the endless loop of run_forever()."""


SETTINGS = Settings(
    link="https://example.test/p",
    api_key="x",
    expected=4,
    unavailability_message="Nicht verfügbar",
    min_interval=30,
    max_interval=90,
)


def page_with(found: int) -> MagicMock:
    page = MagicMock()
    page.find_elements_by_link_text.return_value = [object()] * found
    return page


def make_checker(status=200, found=4, **overrides):
    deps = dict(
        http_get=MagicMock(return_value=MagicMock(status_code=status)),
        open_page=MagicMock(return_value=page_with(found)),
        make_user_agent=MagicMock(return_value="ua"),
        notify=MagicMock(),
        sleep=MagicMock(),
        randint=MagicMock(return_value=45),
    )
    deps.update(overrides)
    return StockChecker(SETTINGS, **deps), deps


def test_timestamp_formats_given_datetime():
    assert timestamp(datetime.datetime(2026, 11, 14, 13, 5, 9)) == "2026-11-14 13:05:09"


def test_timestamp_defaults_to_now():
    assert len(timestamp()) == len("2026-11-14 13:05:09")


@pytest.mark.parametrize("found,expected,changed", [(4, 4, False), (3, 4, True), (0, 4, True)])
def test_is_changed(found, expected, changed):
    assert is_changed(found, expected) is changed


def test_change_message_contains_time_and_link():
    text = change_message("https://x", datetime.datetime(2026, 1, 2, 3, 4, 5))

    assert text == "2026-01-02 03:04:05\nState of your tracked Site has changed:\n https://x"


def test_check_once_returns_none_when_site_is_down(capsys):
    checker, deps = make_checker(status=503)

    assert checker.check_once() is None
    deps["open_page"].assert_not_called()
    deps["notify"].assert_not_called()
    assert deps["sleep"].call_count == 5  # only the response wait


def test_check_once_notifies_on_change(capsys):
    checker, deps = make_checker(found=1)

    assert checker.check_once() is True

    deps["open_page"].assert_called_once_with("https://example.test/p", "ua")
    deps["notify"].assert_called_once()
    assert "State of your tracked Site has changed" in deps["notify"].call_args[0][0]
    assert "Caught change!" in capsys.readouterr().out


def test_check_once_no_notification_when_unchanged():
    checker, deps = make_checker(found=4)

    assert checker.check_once() is False

    deps["notify"].assert_not_called()


def test_check_once_closes_the_browser():
    checker, deps = make_checker(found=4)

    checker.check_once()

    deps["open_page"].return_value.quit.assert_called_once()


def test_check_once_waits_for_response_and_page():
    checker, deps = make_checker(found=4)

    checker.check_once()

    assert deps["sleep"].call_count == 5 + 10


def test_run_forever_waits_random_interval_after_each_check():
    checker, deps = make_checker(found=4)
    deps["sleep"].side_effect = [None] * 15 + [Stop()]

    with pytest.raises(Stop):
        checker.run_forever()

    deps["randint"].assert_called_with(30, 90)
    assert deps["sleep"].call_args_list[-1] == ((45,), {})


def test_run_forever_retries_without_random_wait_when_site_is_down():
    checker, deps = make_checker(status=500)
    deps["sleep"].side_effect = [None] * 5 + [None] * 5 + [Stop()]

    with pytest.raises(Stop):
        checker.run_forever()

    deps["randint"].assert_not_called()
    assert deps["http_get"].call_count == 3  # 5 sleeps per round, stop on the 11th
