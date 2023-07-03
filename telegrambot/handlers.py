import json

import telebot
from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .config import dp, bot
from .services import Service
from .webhook import proceed_update


@csrf_exempt
def telegram_webhook(request):
    # if request.method == 'post':
    try:
        async_to_sync(proceed_update)(request)
    except Exception as e:
        print(e)
    return HttpResponse()


class Handler:
    service = Service()
    admin = '243807051'

    @staticmethod
    @dp.message_handler(commands=["statistic_guests"])
    async def statistic(message: types.Message):
        guests = await sync_to_async(Handler.service.get_all_users)()
        await message.answer(f'По реферальной программе в канал пришло {int(guests)} человек')

    @staticmethod
    @dp.message_handler(commands=["test_working"])
    async def test_working(message: types.Message):
        await message.answer('Работаю штатно')

    @staticmethod
    @dp.chat_join_request_handler()
    async def approve_join_chat(message):
        try:
            await bot.approve_chat_join_request(
                message.chat.id,
                message.from_user.id)

            invite_link = message.invite_link.invite_link[:22]
            user_id = message.from_user.id

            try:
                user_name = message.from_user.username
            except:
                user_name = 'null'

            new_member = await sync_to_async(Handler.service.new_member)(user_id, user_name, invite_link)
            await bot.send_message(Handler.admin, f'new_member: {message.chat.id}, {new_member}')
            if new_member:  # то збс
                await sync_to_async(Handler.service.find_father)(user_id, user_name, invite_link, 0)

        except Exception as ex:
            adm = '243807051'
            await bot.send_message(adm, f'Exception: {ex}')


#
# @csrf_exempt
# def telegram_webhook(request):
#     if request.method == 'POST':
#         update = telebot.types.Update.de_json(request.body.decode('utf-8'))
#         bot.process_new_updates([update])
#         print('post 1234')
#     print(request)
#     return HttpResponse(status=200, )
#
#
# class Handler:
#     bot = bot
#     service = Service()
#     admin = '243807051'
#     """
#     Класс имеет несколько методов. Все принимают только сообщение телеграмм
#
#     1. Посмотреть статистику всех участников, вступивших по реферальной ссылке. Возвращает сообщение с количеством
#      пользователей-участников реф.системы
#     2. Посмотреть работает ли бот. Возвращает сообщение если работает
#     3. Принятие человека в чат/канал.
#     """
#
#     @staticmethod
#     @bot.message_handler(commands=["statistic_guests"])
#     def statistic(message):
#         guests = Handler.service.get_all_users()
#         bot.send_message(message.chat.id, f'По реферальной программе в канал пришло {int(guests)} человек')
#
#     @staticmethod
#     @bot.message_handler(commands=["test_working"])
#     def test_working(message):
#         bot.send_message(message.chat.id, 'Работаю штатно')
#
#     @bot.chat_join_request_handler()
#     def approve_join_chat(self, message):
#         try:
#             bot.approve_chat_join_request(
#                 message.chat.id,
#                 message.from_user.id)
#
#             invite_link = message.invite_link.invite_link[:22]
#             user_id = message.from_user.id
#             user_name = message.from_user.username
#
#             if self.service.new_member(user_id, user_name, invite_link):  # то збс
#                 self.service.find_father(user_id, user_name, invite_link, 0)
#
#         except Exception as ex:
#             bot.send_message(self.admin, f'Exception: {ex}')
#
#
#
