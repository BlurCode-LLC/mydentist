from json import loads
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import TeleBot, types
import requests


bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


@csrf_exempt
def tgbot(request):
    if request.method == "POST":
        result = request.body.decode("UTF-8")
        # result = requests.get("https://api.telegram.org/bot%(token)s/getUpdates" % {
        #     'token': bot.token
        # }).json()
        # print(result)
        update = types.Update.de_json(result)
        bot.process_new_updates([update])

        return JsonResponse(loads(result), status=200)
    return JsonResponse(requests.get("https://api.telegram.org/bot%s/getMe" % bot.token).json(), status=200)


@bot.message_handler(commands=["start"])
def register(message):

    bot.send_message(message.chat.id, "Bot is in the development process")
