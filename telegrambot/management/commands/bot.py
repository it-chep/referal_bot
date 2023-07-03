from django.core.management.base import BaseCommand
from aiogram import executor
from telegrambot.config import dp


class Command(BaseCommand):
    help = '12345'

    def handle(self, *args, **kwargs):
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as ex:
            with open("exceptions.txt", 'w') as f:
                f.write(str(ex))
