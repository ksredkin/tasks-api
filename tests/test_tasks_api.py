from fastapi.testclient import TestClient
from tasks_api.utils.logger import Logger
import unittest

logger = Logger(__name__).get_logger()

class TestTasksAPI(unittest.TestCase):
    @classmethod
    def setUp(cls):
        """Настройка перед каждым тестом"""
        cls.clear_tasks()
    
    @classmethod
    def clear_tasks(cls):
        """Очищает таблицу задач между тестами"""
        import psycopg2
        from tasks_api.utils.env_config import EnvConfig
        
        config = EnvConfig()
        
        conn = psycopg2.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            database=config.get_db_name(),
            user=config.get_db_user(),
            password=config.get_db_password()
        )

        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def setUpClass(cls):
        """Подготовка тестового клиента, временной базы, EnvConfig и JWTManager"""
        import os
        import psycopg2
        
        cls.test_db_name = "tasks_test_db"

        from tasks_api.utils.env_config import EnvConfig
        EnvConfig._instance = None
        os.environ["DB_NAME"] = cls.test_db_name
        config = EnvConfig()
        
        from tasks_api.utils.check_database import check_database
        check_database()

        from tasks_api.utils.jwt import JWTManager
        from tasks_api.main import create_app        

        from tasks_api.repositories.user_repository import UserRepository
        cls.user_id = UserRepository.create_user("test@test.com", "password123")

        JWTManager.set_secret_key("test_secret_key")
        cls.token = JWTManager.create_jwt_token(cls.user_id)
        
        app = create_app()
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        import psycopg2
        from tasks_api.utils.env_config import EnvConfig

        config = EnvConfig()

        conn = psycopg2.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            user=config.get_db_user(),
            password=config.get_db_password(),
            database="postgres"
        )

        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"DROP DATABASE IF EXISTS {cls.test_db_name}")
        cursor.close()
        conn.close()

        import os
        del os.environ["DB_NAME"]

        from tasks_api.utils.env_config import EnvConfig
        from tasks_api.utils.jwt import JWTManager
        EnvConfig._instance = None
        JWTManager._secret_key = None

    def test_create_task_without_auth(self):
        """POST /tasks/ без токена возвращает 401"""
        response = self.client.post("/tasks/", json={"name": "Test", "text": "Test"})
        self.assertEqual(response.status_code, 401)
        logger.info("Тест на ошибку 401 при POST запросе на /tasks/ и отсутствии jwt токена пройден")

    def test_get_tasks_empty(self):
        """GET /tasks/ возвращает пустой список при отсутствии задач"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/tasks/", headers=headers).json()
        
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["data"]["tasks"], [])
        
        logger.info("Тест на возврат пустого списка при GET запросе на /tasks/ с jwt токеном пройден")

    def test_get_task_not_found(self):
        """GET /tasks/999 возвращает 404 для несуществующей задачи"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/tasks/999", headers=headers)
        
        self.assertEqual(response.json()["detail"], "Not found")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Тест на возврат ошибки 404 при GET запросе на /tasks/999 с jwt токеном при отсутствии задачи с id 999 пройден")

    def test_update_task_not_found(self):
        """PUT /tasks/999 возвращает 404 при отсутствии задачи"""
        headers = {"Authorization": f"Bearer {self.token}"}
        json = {"name": "Test1", "text": "TestText", "state": "Done"}
        response = self.client.put("/tasks/999", headers=headers, json=json)
        
        self.assertEqual(response.json()["detail"], "Task not found")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Тест на возврат ошибки 404 при PUT запросе на /tasks/999 с jwt токеном при отсутствии задачи с id 999 пройден")
    
    def test_delete_task_not_found(self):
        """DELETE /tasks/999 возвращает 404"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.delete("/tasks/999", headers=headers)
        
        self.assertEqual(response.json()["detail"], "Task not found")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Тест на возврат ошибки 404 при DELETE запросе на /tasks/999 с jwt токеном при отсутствии задачи с id 999 пройден")
    
    def test_full_crud_cycle(self):
        """Полный цикл: создание -> чтение -> обновление -> удаление"""
        headers = {"Authorization": f"Bearer {self.token}"}

        json_data = {"name": "Test1", "text": "TestText", "state": "Done"}
        response = self.client.post("/tasks/", headers=headers, json=json_data)
        self.assertEqual(response.status_code, 201)
        
        task_data = response.json()
        task_id = task_data["data"]["task"]["id"]
        
        self.assertEqual(task_data["status"], "success")
        self.assertEqual(task_data["data"]["task"]["name"], "Test1")
        
        response = self.client.get("/tasks/", headers=headers)
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["data"]["tasks"][0]["text"], "TestText")
        
        json_data2 = {"name": "Test2", "text": "TestText2", "state": "Done"}
        response3 = self.client.put(f"/tasks/{task_id}", headers=headers, json=json_data2)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.json()["status"], "success")
        self.assertEqual(response3.json()["data"]["task"]["name"], "Test2")
        
        response4 = self.client.get("/tasks/", headers=headers)
        self.assertEqual(response4.json()["status"], "success")
        self.assertEqual(response4.json()["data"]["tasks"][0]["text"], "TestText2")
        
        response5 = self.client.delete(f"/tasks/{task_id}", headers=headers)
        self.assertEqual(response5.status_code, 200)
        self.assertEqual(response5.json()["status"], "success")
        
        logger.info("Тест полного цикла работы TasksRouter пройден")

    def test_cannot_access_other_user_task(self):
        """Пользователь не должен видеть задачи другого пользователя"""
        from tasks_api.repositories.user_repository import UserRepository
        from tasks_api.utils.jwt import JWTManager
        second_user_id = UserRepository.create_user("other@test.com", "password456")
        second_token = JWTManager.create_jwt_token(second_user_id)
        
        task_data = {"name": "Private task", "text": "Only for user 1"}
        response = self.client.post("/tasks/", json=task_data, headers={"Authorization": f"Bearer {self.token}"})
        task_id = response.json()["data"]["task"]["id"]
        
        headers2 = {"Authorization": f"Bearer {second_token}"}
        response = self.client.get(f"/tasks/{task_id}", headers=headers2)
        self.assertEqual(response.status_code, 404)
