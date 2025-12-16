from tasks_api.models.user import User

class UserFactory:
    def create_user(login: str, password: str) -> User:
        return User(login, password)