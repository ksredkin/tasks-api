import unittest

class TestAlembicMigrations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tasks_api.utils.logger import Logger
        cls.logger = Logger(__name__).get_logger()

        from tasks_api.utils.env_config import EnvConfig
        EnvConfig._instance = None

        import os
        os.environ["DB_NAME"] = "test_migrations_db"

        config = EnvConfig()

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
        cursor.execute(f'CREATE DATABASE "{config.get_db_name()}"')
        
        cursor.close()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        from tasks_api.utils.env_config import EnvConfig
        config = EnvConfig()

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

    def test_alembic_migrations(self):
        import subprocess
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)

        from tasks_api.utils.env_config import EnvConfig
        config = EnvConfig()

        import psycopg2
        conn = psycopg2.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            database=config.get_db_name(),
            user=config.get_db_user(),
            password=config.get_db_password()
        )

        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        self.assertEqual(result, [('alembic_version',), ('users',), ('tasks',)])

        result = subprocess.run(["alembic", "downgrade", "base"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)

        conn = psycopg2.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            database=config.get_db_name(),
            user=config.get_db_user(),
            password=config.get_db_password()
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()

        self.assertEqual(result, [('alembic_version',)])

        self.logger.info("Тест миграций прошел успешно.")