from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.logger import Logger
import unittest
from unittest.mock import patch
import os

logger = Logger(__name__).get_logger()

class TestEnvConfig(unittest.TestCase):
    def setUp(self):
        EnvConfig._instance = None

    @classmethod
    def tearDownClass(cls):
        patch.stopall()
        EnvConfig._instance = None

    @patch("tasks_api.utils.env_config.os.getenv")
    def test_singleton_pattern(self, mock_getenv):
        mock_getenv.return_value = "your_super_secret_key_here_must_be_at_least_32_chars"

        config1 = EnvConfig()
        config2 = EnvConfig()

        self.assertIs(config1, config2)
        logger.info("Тест на singleton пройден")

    @patch('tasks_api.utils.env_config.os.getenv')
    def test_no_db_data(self, mock_getenv):
        mock_getenv.return_value = None

        with self.assertRaises(ValueError) as context:
            config = EnvConfig()

        self.assertEqual(str(context.exception), "Отсутствуют переменные окружения: ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']")
        logger.info("Тест на отсутствие SECRET_KEY пройден")

    @patch.dict(os.environ, {"SECRET_KEY": "your_super_secret_key_here_must_be_at_least_32_chars"})
    def test_secret_key_exists(self):
        config = EnvConfig()
        secret_key = config.get_secret_key()

        self.assertEqual(secret_key, "your_super_secret_key_here_must_be_at_least_32_chars")
        logger.info("Тест на наличие SECRET_KEY пройден")