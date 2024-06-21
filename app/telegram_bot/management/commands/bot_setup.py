# Python imports
import asyncio

# Django imports
from django.core.management.base import BaseCommand

# Telegram imports
from aiogram import Dispatcher


# import Bot object
from main.settings import bot

dp = Dispatcher()


#  https://docs.aiogram.dev/en/stable/#simple-usage
async def main() -> None:
    """
    Ф-ция запускает работу бота.
    """
    print('bot go')
    await dp.start_polling(bot)


class Command(BaseCommand):
    """
    Запускает бот-пуллинг телеграмм-бота
    """

    def handle(self, *args, **options):

        asyncio.run(main())
