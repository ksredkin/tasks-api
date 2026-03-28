from tasks_api.api.routes.tasks_router import tasks_router
from tasks_api.api.routes.user_router import user_router
from tasks_api.api.routes.folders_router import folders_router
from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.jwt import JWTManager
from tasks_api.utils.logger import Logger
from fastapi import FastAPI
import uvicorn
import os

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(tasks_router)
    app.include_router(user_router)
    app.include_router(folders_router)
    return app

def configure_app(app: FastAPI):
    env_config = EnvConfig()
    JWTManager.set_secret_key(env_config.get_secret_key())

def start_api():
    try:
        logger = Logger(__name__).get_logger()

        app = create_app()        
        configure_app(app)
        
        api_host = os.getenv("API_HOST")
        api_port = int(os.getenv("API_PORT"))

        logger.info(f"API запускается на {api_host}:{api_port}")
        uvicorn.run(app, host=api_host, port=api_port)

    except Exception as e:
        logger.critical(f"Не удалось запустить API: {e}")
        raise

if __name__ == "__main__":
    start_api()