from bot.utils.env_config import EnvConfig
from bot.utils.logger import Logger
import httpx

logger = Logger(__name__).get_logger()

class APIClient:
    @staticmethod
    async def get_user_tasks(user_token: str) -> list[dict] | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/tasks/"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers)
                data = response.json()
                if isinstance(data, list):
                    return data
                return None
            
        except Exception as e:
            logger.info(f"Ошибка при получении задач от API: {e}")
            return None
        
    @staticmethod
    async def get_user_task_by_id(user_token: str, task_id: int) -> dict | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/tasks/{task_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers)
                return response.json()
            
        except Exception as e:
            logger.info(f"Ошибка при получении задачи от API: {e}")
            return None
        
    @staticmethod
    async def create_task(user_token: str, task_name: str, task_text: str, folder_id: int = 0) -> list[dict] | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/tasks/"
        json = {"name": task_name, "text": task_text, "state": "Active", "folder_id": folder_id if folder_id else None}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=json)
                data = response.json()
                return data
            
        except Exception as e:
            logger.info(f"Ошибка при запросе создания задачи к API: {e}")
            return None
    
    @staticmethod
    async def update_task(user_token: str, task_id: int, task_name: str|None = None, task_text: str|None = None, task_state: str|None = None, folder_id: int|None = None) -> dict | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/tasks/{task_id}"
        json = {"state": "Active" if task_state is None else task_state}
        current_task = await APIClient.get_user_task_by_id(user_token, task_id)
        json["name"] = task_name if task_name else current_task.get("name")
        json["text"] = task_text if task_text else current_task.get("text")
        json["folder_id"] = folder_id if folder_id else current_task.get("folder_id")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(url=url, headers=headers, json=json)
                return response.json()
        
        except Exception as e:
            logger.info(f"Ошибка при запросе обновления задачи к API: {e}")
            return None
        
    @staticmethod
    async def update_folder(user_token: str, folder_id: int, folder_name: str|None = None, parent_id: int|None = None, show_progress: bool|None = None) -> dict | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/{folder_id}"
        json = {}
        current_folder = await APIClient.get_user_folder_by_id(user_token, folder_id)
        json["name"] = folder_name if folder_name else current_folder.get("name")
        json["text"] = show_progress if show_progress else current_folder.get("text")
        json["parent_id"] = parent_id if parent_id else current_folder.get("parent_id")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(url=url, headers=headers, json=json)
                return response.json()
        
        except Exception as e:
            logger.info(f"Ошибка при запросе обновления задачи к API: {e}")
            return None

    @staticmethod
    async def delete_task(user_token: str, task_id: int) -> list[dict] | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/tasks/{task_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(url=url, headers=headers)
                return response.json()
        
        except Exception as e:
            logger.info(f"Ошибка при запросе удаления задачи к API: {e}")
            return None
        
    @staticmethod
    async def login(user_login: str, user_password: str) -> str | None:
        config = EnvConfig()
        json = {"login": user_login, "password": user_password}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/user/login"
        try:
            async with httpx.AsyncClient() as client:      
                response = await client.post(url=url, json=json)
                data = response.json()
                return data.get("data").get("access_token")
            
        except Exception as e:
            logger.info(f"Ошибка при запросе входа к API: {e}")
            return None
        
    @staticmethod
    async def register(user_login: str, user_password: str) -> bool:
        config = EnvConfig()
        json = {"login": user_login, "password": user_password}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/user/register"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, json=json)
                data = response.json()
                return True if data.get("id") != None else False
        
        except Exception as e:
            logger.info(f"Ошибка при запросе рагистрации к API: {e}")
            return False
        
    @staticmethod
    async def get_user_folders(user_token: str) -> list[dict] | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers)
                data = response.json()
                if isinstance(data, list):
                    return data
                return None
            
        except Exception as e:
            logger.info(f"Ошибка при получении задач от API: {e}")
            return None
        
    @staticmethod
    async def get_user_folder_by_id(user_token: str, folder_id: int) -> list[dict] | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/{folder_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers)
                data = response.json()
                return data
        
        except Exception as e:
            logger.info(f"Ошибка при получении задач от API: {e}")
            return None

    @staticmethod
    async def get_user_folders_in_folder(user_token: str, folder_id: int) -> list[dict] | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/{folder_id}/folders"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers)
                data = response.json()
                if isinstance(data, list):
                    return data
                return None
            
        except Exception as e:
            logger.info(f"Ошибка при получении задач от API: {e}")
            return None
        
    @staticmethod
    async def get_user_tasks_in_folder(user_token: str, folder_id: int) -> list[dict] | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/{folder_id}/tasks"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers)
                data = response.json()
                if isinstance(data, list):
                    return data
                return None
            
        except Exception as e:
            logger.info(f"Ошибка при получении задач от API: {e}")
            return None
        
    @staticmethod
    async def create_folder(user_token: str, name: str, parent_id: int = None, show_progress: bool = False) -> dict | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/"
        json = {"name": name, "parent_id": parent_id if parent_id != 0 else None, "show_progress": show_progress}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=json)
                data = response.json()
                return data
            
        except Exception as e:
            logger.info(f"Ошибка при запросе создания задачи к API: {e}")
            return None
        
    @staticmethod
    async def delete_folder(user_token: str, folder_id: int) -> dict | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/{folder_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(url, headers=headers)
                data = response.json()
                return data
            
        except Exception as e:
            logger.info(f"Ошибка при запросе создания задачи к API: {e}")
            return None
        
    @staticmethod
    async def get_folder_progress(user_token: str, folder_id: int) -> dict | None:
        config = EnvConfig()
        headers = {"Authorization": f"Bearer {user_token}"}
        url = f"http://{config.get_api_host()}:{config.get_api_port()}/folders/{folder_id}/progress"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                data = response.json()
                return data
            
        except Exception as e:
            logger.info(f"Ошибка при запросе создания задачи к API: {e}")
            return None