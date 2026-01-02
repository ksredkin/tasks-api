import unittest
from unittest.mock import patch, Mock
from tasks_api.services.user_service import UserService
from tasks_api.utils.logger import Logger
from tasks_api.services.user_service import context
from tasks_api.utils.jwt import JWTManager
from types import NoneType

logger = Logger(__name__).get_logger()

class TestUserService(unittest.TestCase):
    def setUp(self):
        patch.stopall()     

    @classmethod
    def tearDownClass(cls):
        patch.stopall()
        JWTManager._secret_key = None

    @patch("tasks_api.services.user_service.UserRepository.get_user_password")
    def test_create_new_user_if_exists(self, mock_get_user_password):
        mock_get_user_password.return_value = ["test_password", ]

        result = UserService.create_new_user("string", "test_password2")
        
        self.assertEqual(result, False)
        mock_get_user_password.assert_called_once_with("string")
        
        logger.info("Тест на отсутствие создания пользователя, если он уже есть в базе, пройден")

    @patch("tasks_api.services.user_service.UserRepository")
    def test_create_new_user(self, mock_user_repo):
        mock_user_repo.get_user_password.return_value = None
        mock_user_repo.create_user.return_value = None

        result = UserService.create_new_user("test_login", "test_password")
        self.assertEqual(result, True)

        mock_user_repo.get_user_password.assert_called_once_with("test_login")
        mock_user_repo.create_user.assert_called_once()

        logger.info("Тест на создание пользователя пройден")

    @patch("tasks_api.services.user_service.UserRepository")
    def test_login_if_user_not_exists(self, user_repo):
        user_repo.get_user_password.return_value = None

        result = UserService.login("test_login", "test_password")

        self.assertEqual(result, None)

        logger.info("Тест на вход в несуществующий аккаунт пройден")

    @patch("tasks_api.services.user_service.UserRepository")
    def test_login_if_password_is_incorrect(self, user_repo):
        user_repo.get_user_password.return_value = context.hash("test_password")
        user_repo.get_user_id.return_value = 1

        JWTManager.set_secret_key("your_super_secret_key_here_must_be_at_least_32_chars")

        result = UserService.login("test_login", "test_password2")

        self.assertIsInstance(result, NoneType)

        logger.info("Тест на вход в несуществующий аккаунт пройден")

    @patch("tasks_api.services.user_service.UserRepository")
    def test_login(self, user_repo):
        user_repo.get_user_password.return_value = context.hash("test_password")
        user_repo.get_user_id.return_value = 1

        JWTManager.set_secret_key("your_super_secret_key_here_must_be_at_least_32_chars")

        result = UserService.login("test_login", "test_password")

        self.assertIsInstance(result, str)

        logger.info("Тест на вход в аккаунт пройден")