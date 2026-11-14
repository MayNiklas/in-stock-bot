"""Runtime settings, read from environment variables."""
import os
from dataclasses import dataclass
from typing import Mapping, Optional

DEFAULT_MIN_INTERVAL = 30
DEFAULT_MAX_INTERVAL = 90


@dataclass(frozen=True)
class Settings:
    link: str
    api_key: str
    expected: int
    unavailability_message: str
    min_interval: int = DEFAULT_MIN_INTERVAL
    max_interval: int = DEFAULT_MAX_INTERVAL

    @classmethod
    def from_env(cls, env: Optional[Mapping[str, str]] = None) -> "Settings":
        env = os.environ if env is None else env
        return cls(
            link=env['LINK'],
            api_key=env['API_Key'],
            expected=int(env['expected']),
            unavailability_message=env['unavailabilityMessage'],
            min_interval=int(env.get('min_interval', DEFAULT_MIN_INTERVAL)),
            max_interval=int(env.get('max_interval', DEFAULT_MAX_INTERVAL)),
        )
