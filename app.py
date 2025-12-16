from tasks_api.main import start_api
from tasks_api.utils.check_database import check_database

def main():
    # Tests in future
    check_database()
    start_api()

if __name__ == "__main__":
    main()