import asyncio
from bot.utils.logger import Logger
from bot.utils.api_client import APIClient
from bot.core.config import UPDATE_REPEAT_TASKS_INTERVAL

logger = Logger(__name__).get_logger()

async def update_tasks_service():
    while True:
        try:
            await asyncio.sleep(UPDATE_REPEAT_TASKS_INTERVAL)
            is_success = await APIClient.update_repeat_tasks()

            if is_success:
                logger.info("Успешно обновлены повторяющиеся задачи.")
                continue
            
            logger.critical(f"Не удалось обновить повторяющиеся задачи")

        except Exception as e:
            logger.critical(f"Не удалось обновить повторяющиеся задачи: {e}")