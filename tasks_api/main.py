from fastapi import FastAPI
import uvicorn
from tasks_api.core.config import *
from tasks_api.api.routes.tasks_router import tasks_router
from tasks_api.api.routes.user_router import user_router
from tasks_api.utils.env_config import EnvConfig
from tasks_api.utils.jwt import JWTManager

def start_api():
    app = FastAPI()
    app.include_router(tasks_router)
    app.include_router(user_router)
    env_config = EnvConfig()
    JWTManager.set_secret_key(env_config.get_secret_key())
    uvicorn.run(app, host=API_HOST, port=API_PORT)

if __name__ == "__main__":
    start_api()