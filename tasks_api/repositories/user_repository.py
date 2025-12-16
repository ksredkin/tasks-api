from tasks_api.utils.execute_query import execute_query

class UserRepository:
    def create_user(login: str, password: str) -> str | None:
        user_id = execute_query("INSERT INTO users (login, password) VALUES (?, ?) RETURNING id", (login, password))
        return user_id[0][0] if user_id else None
    
    def get_user_password(login: str) -> str | None:
        user_password = execute_query("SELECT password FROM users WHERE login=?", (login,))
        return user_password[0][0] if user_password else None
    
    def get_user_id(login: str) -> int | None:
        user_id = execute_query("SELECT id FROM users WHERE login=?", (login,))
        return user_id[0][0] if user_id else None
    
    def get_user_login(id: int) -> str | None:
        user_login = execute_query("SELECT login FROM users WHERE id=?", (id,))
        return user_login[0][0] if user_login else None