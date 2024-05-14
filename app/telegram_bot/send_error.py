# Python imports
import os
import logging

# import telegram bot
from main.settings import bot

logger = logging.getLogger(__name__)


async def telegram_log_errors(exception_text: str):
    """ для логгирования событий """
    try:
        await bot.send_message(
            chat_id=os.getenv("DEVELOPER_TELEGRAM_ID"),
            text=exception_text
        )

    except Exception as ex:
        # FIXME: заменить/добавить логгирование в файл, logging
        logger.error(f"[telegram_log_errors] {ex}")
    logger.error(exception_text)
