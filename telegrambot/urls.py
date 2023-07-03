from django.conf import settings

from .views import *
from django.urls import path
from .handlers import telegram_webhook

urlpatterns = [
    path('referals/', Referals.as_view(), name='referals'),
    path('users/', Users.as_view(), name='users'),
    path(f'{settings.BOT_TOKEN}/', telegram_webhook, name='bot'),

    path('', MainPage.as_view(), name='main'),
]
