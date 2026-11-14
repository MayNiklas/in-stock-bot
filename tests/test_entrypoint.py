import importlib


def test_entrypoint_delegates_to_app_main():
    entry = importlib.import_module("in-stock")
    app = importlib.import_module("app")

    assert entry.main is app.main
