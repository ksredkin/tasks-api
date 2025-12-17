from tasks_api.api.routes.tasks_router import tasks_router
from tasks_api.api.routes.user_router import user_router
from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.jwt import JWTManager
from tasks_api.utils.logger import Logger
from tasks_api.core.config import *
from fastapi import FastAPI
import uvicorn

def start_api():
    try:
        logger = Logger(__name__).get_logger()

        app = FastAPI()
        
        app.include_router(tasks_router)
        app.include_router(user_router)
        
        env_config = EnvConfig()
        JWTManager.set_secret_key(env_config.get_secret_key())
        
        logger.info(f"API запускается на {API_HOST}:{API_PORT}")
        uvicorn.run(app, host=API_HOST, port=API_PORT)

    except Exception as e:
        logger.critical(f"Не удалось запустить API: {e}")
        raise

if __name__ == "__main__":
    start_api()