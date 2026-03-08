from datetime import datetime, timedelta, timezone
from tasks_api.core.config import MINUTES_TO_RESET_LOGIN_ATTEMPTS

class AttemptsStorage:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._attempts = {}
        return cls._instance

    def is_expired(self, last_time: datetime) -> bool:
        return datetime.now(timezone.utc) - last_time > timedelta(minutes=MINUTES_TO_RESET_LOGIN_ATTEMPTS)

    def add_attempt(self, ip: str, login: str):
        key = (ip, login)

        attempts, last_time = self._attempts.get(key, (0, None))

        if last_time and self.is_expired(last_time):
            attempts = 0

        self._attempts[key] = (attempts + 1, datetime.now(timezone.utc))

    def get_attempts(self, ip: str, login: str) -> int:
        key = (ip, login)

        data = self._attempts.get(key)

        if data is None:
            return 0

        attempts, last_time = data

        if self.is_expired(last_time):
            self._attempts.pop(key, None)
            return 0

        return attempts

    def reset_attempts(self, ip: str, login: str):
        self._attempts.pop((ip, login), None)