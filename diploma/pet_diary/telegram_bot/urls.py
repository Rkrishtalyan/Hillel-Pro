from django.urls import path
from telegram_bot.views import telegram_webhook

urlpatterns = [
    path('telegram-webhook/<str:token>/', telegram_webhook, name='telegram_webhook'),
]
