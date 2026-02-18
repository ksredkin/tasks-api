from tasks_api.utils.logger import Logger
import unittest

def run_tests():
    try:
        logger = Logger(__name__).get_logger()
        logger.info("Тесты запущены")

        loader = unittest.TestLoader()
    
        suite = loader.discover('tests', pattern='test_*.py')
            
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        if not result.wasSuccessful():
            raise Exception("Тесты не пройдены")
        
        logger.info("Тесты успешно пройдены")

    except Exception as e:
        logger.critical(f"Произошла ошибка при выполнении тестов: {e}")
        raise

if __name__ == "__main__":
    run_tests()