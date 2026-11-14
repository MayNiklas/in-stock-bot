import dataclasses

import pytest

from config import Settings

BASE_ENV = {
    "LINK": "https://example.test/p",
    "API_Key": "123:TEST",
    "expected": "4",
    "unavailabilityMessage": "Nicht verfügbar",
}


def test_from_env_uses_defaults_for_intervals():
    settings = Settings.from_env(BASE_ENV)

    assert settings == Settings(
        link="https://example.test/p",
        api_key="123:TEST",
        expected=4,
        unavailability_message="Nicht verfügbar",
        min_interval=30,
        max_interval=90,
    )


def test_from_env_reads_intervals():
    env = {**BASE_ENV, "min_interval": "60", "max_interval": "120"}

    settings = Settings.from_env(env)

    assert (settings.min_interval, settings.max_interval) == (60, 120)


def test_from_env_defaults_to_os_environ(monkeypatch):
    for key, value in BASE_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("min_interval", raising=False)
    monkeypatch.delenv("max_interval", raising=False)

    settings = Settings.from_env()

    assert settings.link == "https://example.test/p"
    assert settings.max_interval == 90


def test_from_env_missing_required_variable_raises():
    env = dict(BASE_ENV)
    del env["LINK"]

    with pytest.raises(KeyError):
        Settings.from_env(env)


def test_settings_are_immutable():
    settings = Settings.from_env(BASE_ENV)

    with pytest.raises(dataclasses.FrozenInstanceError):
        settings.expected = 5
