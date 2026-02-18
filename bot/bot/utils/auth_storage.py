class AuthStorage:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._tokens = {}
        return cls._instance
    
    def set_token(self, telegram_id: int, token: str):
        self._tokens[telegram_id] = token

    def get_token(self, telegram_id: int) -> str | None:
        return self._tokens.get(telegram_id, None)
    
    def delete_token(self, telegram_id: int):
        self._tokens.pop(telegram_id)