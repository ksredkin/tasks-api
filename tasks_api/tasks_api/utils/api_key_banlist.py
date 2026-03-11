class ApiKeyBanlist:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._banlist = []
        return cls._instance

    def add_ip(self, ip: str):
        self._banlist.append(ip)

    def is_in_banlist(self, ip: str) -> bool:
        return ip in self._banlist