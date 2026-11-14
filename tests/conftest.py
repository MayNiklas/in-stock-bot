import os
import sys
from unittest.mock import MagicMock

# Environment expected by src/in-stock.py at import time
os.environ.setdefault("LINK", "https://example.test/product")
os.environ.setdefault("API_Key", "123:TEST")
os.environ.setdefault("expected", "4")
os.environ.setdefault("unavailabilityMessage", "Nicht verfügbar")

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC)

# Third-party packages are replaced by mocks so the tests need no network,
# no Telegram token and no Chrome/chromedriver.
for name in [
    "requests",
    "telegram",
    "telegram.ext",
    "fake_headers",
    "selenium",
    "selenium.webdriver",
    "selenium.webdriver.remote",
    "selenium.webdriver.remote.webelement",
]:
    sys.modules[name] = MagicMock()

sys.modules["fake_headers"].Headers.return_value.generate.return_value = {"User-Agent": "test-agent"}
