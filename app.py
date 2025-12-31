from tasks_api.utils.check_database import check_database
from tasks_api.utils.logger import Logger
from tests.run_tests import run_tests
from tasks_api.main import start_api

def main():
    try:
        logger = Logger(__name__).get_logger()
        logger.info("Запуск TasksAPI..")
        run_tests()
        check_database()
        start_api()
        logger.info("Завершение работы TasksAPI..")
        
    except Exception as e:
        logger.critical(f"Не удалось запустить: {e}")
        raise

if __name__ == "__main__":
    main()