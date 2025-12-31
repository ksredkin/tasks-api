from tasks_api.utils.execute_query import execute_query

class TasksRepository:
    def get_user_tasks(id: int) -> str | None:
        user_tasks = execute_query("SELECT id, name, text, state, date FROM tasks WHERE user_id=?", (id,))
        return user_tasks if user_tasks else None
    
    def get_user_task(task_id: int, user_id: int) -> str | None:
        user_task = execute_query("SELECT name, text, state, date FROM tasks WHERE user_id=? AND id=?", (user_id, task_id))
        print(user_task)
        return user_task[0] if user_task else None
    
    def create_task(user_id: int, name: str, text: str, state: str) -> tuple | None:
        result = execute_query("INSERT INTO tasks (user_id, name, text, state, date) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP) RETURNING id, date", (user_id, name, text, state))
        return (result[0][0], result[0][1]) if result else None
    
    def update_task(user_id: int, task_id: str, name: str, text: str, state: str) -> str | None:
        date = execute_query("UPDATE tasks SET name=?, text=?, state=?, date=CURRENT_TIMESTAMP WHERE user_id=? AND id=? RETURNING date", (name, text, state, user_id, task_id))
        return date[0][0] if date else None
    
    def delete_task(user_id: int, task_id: str) -> tuple | None:
        task = execute_query("DELETE FROM tasks WHERE user_id=? AND id=? RETURNING name, text, state, date", (user_id, task_id))
        print(task)
        return task[0] if task else None