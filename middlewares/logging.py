import time
from typing import Callable, Dict, Any, Awaitable, reveal_type

from aiogram import BaseMiddleware
from aiogram.types import Update

from utils.logging import get_logger


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ):
        logger = get_logger()
        # Время INFO MESSAGE время отработки (кто это отправил)
        start_time=time.time()
        response = await handler(event, data)
        end_time = (time.time() - start_time) * 1000
        event_name = "MESSAGE" if event.message else "CALLBACK"
        logger.info(
            f"{event_name}: {end_time}ms",
        )
        return response