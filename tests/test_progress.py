from unittest.mock import MagicMock

from progress import progbar, wait_with_progress


def test_progbar_yields_each_step(capsys):
    assert list(progbar(3, "wait")) == [0, 1, 2]
    assert "3/3 wait" in capsys.readouterr().out


def test_wait_with_progress_sleeps_one_second_per_step(capsys):
    sleep = MagicMock()

    wait_with_progress(4, "loading", sleep)

    assert sleep.call_count == 4
    sleep.assert_called_with(1)
    assert "4/4 loading" in capsys.readouterr().out


def test_wait_with_progress_zero_seconds_does_not_sleep():
    sleep = MagicMock()

    wait_with_progress(0, "nothing", sleep)

    sleep.assert_not_called()
