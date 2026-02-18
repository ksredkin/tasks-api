from unittest.mock import patch, Mock
from tasks_api.services.auth_service import AuthService
from tasks_api.utils.jwt import JWTManager
from tasks_api.utils.logger import Logger
from fastapi import HTTPException
import unittest

logger = Logger(__name__).get_logger()

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        JWTManager.set_secret_key("your_super_secret_key_here_must_be_at_least_32_chars")
        self.auth_service = AuthService(self.mock_repo)
        patch.stopall()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()
        JWTManager._secret_key = None

    def test_get_current_user_valid(self):
        test_user_id = 1
        token = JWTManager.create_jwt_token(test_user_id)

        mock = Mock()
        mock.id = test_user_id
        mock.login = "test_login"
        mock.password = "test_password"

        self.mock_repo.get_user_by_id.return_value = mock

        result = self.auth_service._get_user_id_from_token(token)

        self.assertEqual(result, 1)
        self.mock_repo.get_user_by_id.assert_called_once_with(str(test_user_id))
        logger.info("Тест на извлечение user_id из jwt токена пройден")

    def test_get_current_user_not_found(self):
        test_user_id = 1
        token = JWTManager.create_jwt_token(test_user_id)

        self.mock_repo.get_user_by_id.return_value = None

        with self.assertRaises(HTTPException) as context:
            self.auth_service._get_user_id_from_token(token)

        self.assertEqual(context.exception.status_code, 401)
        self.mock_repo.get_user_by_id.assert_called_once_with(str(test_user_id))
        logger.info("Тест на ошибку при несуществующем user_id пройден")