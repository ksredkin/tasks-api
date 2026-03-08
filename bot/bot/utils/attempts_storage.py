class AttemptsStorage:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._attempts = {}
        return cls._instance
    
    def add_attempt(self, telegram_id: int, login: str):
        self._attempts[(telegram_id, login)] = 1 if self._attempts.get((telegram_id, login)) is None else self._attempts.get((telegram_id, login)) + 1

    def get_attempts(self, telegram_id: int, login: str) -> int:
        return self._attempts.get((telegram_id, login), 0)
    
    def reset_attempts(self, telegram_id: int, login: str):
        if (telegram_id, login) in self._attempts.keys():
            self._attempts.pop((telegram_id, login))