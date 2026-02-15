import unittest

class TestOrmRepositories(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tasks_api.utils.logger import Logger
        cls.logger = Logger(__name__).get_logger()

        from tasks_api.utils.env_config import EnvConfig
        EnvConfig._instance = None

        import os
        os.environ["DB_NAME"] = "test_orm_repositories_db"

        config = EnvConfig()

        from tasks_api.database.connection import db
        db.reconnect()

        cls.logger.info("-"*40 + config.get_db_name())

        from tasks_api.utils.check_database import check_database
        check_database()

        cls.test_task_name = "test_task_name"
        cls.test_task_text = "test_task_text"
        cls.test_task_state = "test_task_state"

    @classmethod
    def tearDownClass(cls):
        from tasks_api.utils.env_config import EnvConfig
        config = EnvConfig()

        from tasks_api.database.connection import db
        db.reset()
        
        import psycopg2
        conn = psycopg2.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            database="postgres",
            user=config.get_db_user(),
            password=config.get_db_password()
        )

        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f'DROP DATABASE "{config.get_db_name()}"')
        
        cursor.close()
        conn.close()

        EnvConfig._instance = None

        import os
        del os.environ["DB_NAME"]

        db.reconnect()

    def test_create_user(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_create_user"
        user = OrmUserRepository.create_user(test_user_login, "test_password")

        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.login, test_user_login)

        self.logger.info("Тест репозитория на создание пользователя пройден")

    def test_get_user_by_login(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_get_user_by_login"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        getted_user = OrmUserRepository.get_user_by_login(test_user_login)
        self.assertIsNotNone(getted_user)
        self.assertEqual(getted_user.id, user.id)

        self.logger.info("Тест репозитория на получение пользователя по login пройден")

    def test_get_user_id_by_login(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_get_user_id_by_login"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        getted_id = OrmUserRepository.get_user_id_by_login(test_user_login)
        self.assertIsNotNone(getted_id)
        self.assertEqual(getted_id, user.id)

        self.logger.info("Тест репозитория на получение id пользователя по login пройден")

    def test_get_user_password_by_login(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_get_user_password_by_login"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        getted_password = OrmUserRepository.get_user_password_by_login(test_user_login)
        self.assertIsNotNone(getted_password)
        self.assertEqual(getted_password, user.password)

        self.logger.info("Тест репозитория на получение пароля пользователя по login пройден")

    def test_create_task(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_create_task"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        from tasks_api.repositories.orm_task_repository import OrmTaskRepository
        
        task = OrmTaskRepository.create_task(user.id, self.test_task_name, self.test_task_text, self.test_task_state)
        
        self.assertIsNotNone(task)
        self.assertEqual(task.name, self.test_task_name)
        self.assertEqual(task.text, self.test_task_text)
        self.assertEqual(task.state, self.test_task_state)
        self.assertEqual(task.user_id, task.user_id)

        self.logger.info("Тест репозитория на создание задачи пройден")

    def test_get_user_tasks(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_get_user_tasks"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        from tasks_api.repositories.orm_task_repository import OrmTaskRepository
        task = OrmTaskRepository.create_task(user.id, self.test_task_name, self.test_task_text, self.test_task_state)
        self.assertIsNotNone(task)

        user_tasks = OrmTaskRepository.get_user_tasks(user.id)
        self.assertEqual(user_tasks[0].name, self.test_task_name)
        self.assertEqual(user_tasks[0].state, self.test_task_state)
        self.assertEqual(user_tasks[0].text, self.test_task_text)

        self.logger.info("Тест репозитория на получение всех задач пройден")

    def test_get_user_task_by_id(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_get_user_task_by_id"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        from tasks_api.repositories.orm_task_repository import OrmTaskRepository
        task = OrmTaskRepository.create_task(user.id, self.test_task_name, self.test_task_text, self.test_task_state)
        self.assertIsNotNone(task)

        user_task = OrmTaskRepository.get_user_task_by_id(user.id, task.id)
        self.assertEqual(user_task.name, self.test_task_name)
        self.assertEqual(user_task.state, self.test_task_state)
        self.assertEqual(user_task.text, self.test_task_text)

        self.logger.info("Тест репозитория на получение задачи по id пройден")

    def test_update_task(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_update_task"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        from tasks_api.repositories.orm_task_repository import OrmTaskRepository
        task = OrmTaskRepository.create_task(user.id, self.test_task_name, self.test_task_text, self.test_task_state)
        self.assertIsNotNone(task)

        new_test_task_name = "new_test_update_task_name"
        new_test_task_text = "new_test_update_task_text"
        new_test_task_state = "new_test_update_task_state"
        user_task = OrmTaskRepository.update_task(user.id, task.id, new_test_task_name, new_test_task_text, new_test_task_state)
        self.assertEqual(user_task.name, new_test_task_name)
        self.assertEqual(user_task.state, new_test_task_state)
        self.assertEqual(user_task.text, new_test_task_text)

        self.logger.info("Тест репозитория на обновление задачи пройден")

    def test_delete_task(self):
        from tasks_api.repositories.orm_user_repository import OrmUserRepository
        test_user_login = "test_delete_task"
        user = OrmUserRepository.create_user(test_user_login, "test_password")
        self.assertIsNotNone(user)

        from tasks_api.repositories.orm_task_repository import OrmTaskRepository
        task = OrmTaskRepository.create_task(user.id, self.test_task_name, self.test_task_text, self.test_task_state)
        self.assertIsNotNone(task)

        result = OrmTaskRepository.delete_task(user.id, 100)
        self.assertEqual(result, None)

        user_task = OrmTaskRepository.delete_task(user.id, task.id)
        self.assertEqual(user_task.name, self.test_task_name)
        self.assertEqual(user_task.state, self.test_task_state)
        self.assertEqual(user_task.text, self.test_task_text)
        self.assertEqual(user_task.id, task.id)

        self.logger.info("Тест репозитория на удаление задачи пройден")