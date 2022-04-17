import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.distance import distance
from json import loads
from random import randrange
from telebot import TeleBot, types

from . import keypad
from .models import User
from .utils import *


bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


@csrf_exempt
def tgbot(request):
    if request.method == "POST":
        result = request.body.decode("utf-8")
        update = types.Update.de_json(loads(result))
        bot.process_new_updates([update])

        return HttpResponse("")
    return JsonResponse(requests.get("https://api.telegram.org/bot%s/getMe" % bot.token).json(), status=200)


with open("bot/string_file.json", "r", encoding="utf-8") as file:
    str_obj = loads(file.read())


global language
language = ""

global status
status = ""

global page
page = 0


def price_splitter(price):
    new_price = ""
    i = 0
    if len(price) % 3 == 1:
        new_price += price[0:1]
        i += 1
    elif len(price) % 3 == 2:
        new_price += price[0:2]
        i += 2
    while i != len(price):
        if new_price == "":
            new_price += price[i:(i + 3)]
        else:
            new_price += f" {price[i:(i + 3)]}"
        i += 3
    return new_price


def oscilate(distance):
    return round(distance + randrange(500, 2000, 10) / 1000, 2)


def register_checker(bot, message):
    user = User.objects.create(
        name=message.chat.first_name,
        lastname=message.chat.last_name,
        tg_user_id=message.chat.id
    )
    language = "uz"
    status = "start"
    bot.send_message(message.chat.id, "Tilni tanlang:\nВыберите язык:", reply_markup=keypad.reply_buttons(language, message.chat.id, status))


def sort_by_distance(user, dentists):
    if len(dentists) < 2:
        return dentists
    else:
        pivot = dentists[0]
        less = [
            i for i in dentists[1:]
            if distance(
                (i["latitude"], i["longitude"]),
                (user["latitude"], user["longitude"])
            ).kilometers <= distance(
                (pivot["latitude"], pivot["longitude"]),
                (user["latitude"], user["longitude"])
            ).kilometers
        ]
        greater = [
            i for i in dentists[1:]
            if distance(
                (i["latitude"], i["longitude"]),
                (user["latitude"], user["longitude"])
            ).kilometers > distance(
                (pivot["latitude"], pivot["longitude"]),
                (user["latitude"], user["longitude"])
            ).kilometers
        ]
        return sort_by_distance(user, less) + [pivot] + sort_by_distance(user, greater)


def dentists_by_location(str_obj, language, location, dentists, page=1):
    location = (float(location["latitude"]), float(location["longitude"]))
    text = []
    count = (page - 1) * 4
    if page * 4 >= len(dentists):
        start = (page - 1) * 4
        dentists_temp = dentists[start:]
    else:
        start = (page - 1) * 4
        stop = page * 4
        dentists_temp = dentists[start: stop]
    i = 0
    for dentist in dentists_temp:
        text1 = f"<b>{str_obj[language]['result_template'][0].upper()}{str(count + 1)}</b>   🦷 🦷 🦷 🦷 🦷\n\n"
        text1 += f"<b>{dentist['name']}</b>\n"
        text1 += f"<a href=\"{dentist['tg_href']}\">{dentist['fullname']}</a>\n"
        text1 += f"<b>{str_obj[language]['result_template'][9]}:</b> {dentist['worktime']}\n"
        lat = float(dentist["latitude"])
        long = float(dentist["longitude"])
        loc = (lat, long)
        text1 += f"{dentist['address']} ({str(oscilate(round(distance(location, loc).kilometers, 2)))} {str_obj[language]['result_template'][7]}).  <a href=\"https://maps.google.com/maps?q={str(lat)},{str(long)}&ll={str(lat)},{str(long)}&z=16\">🗺 {str_obj[language]['result_template'][13]}</a>\n"
        text1 += f"{dentist['phone_number']}\n\n\n"
        count += 1
        i += 1
        text.append(text1)
    text.append("@MyDentistUzBot")
    return "".join(text)


def dentists_by_price(str_obj, language, message, location, dentists, page=1):
    location = (float(location["latitude"]), float(location["longitude"]))
    text = []
    count = (page - 1) * 4
    if page * 4 >= len(dentists):
        start = (page - 1) * 4
        dentists_temp = dentists[start:]
    else:
        start = (page - 1) * 4
        stop = page * 4
        dentists_temp = dentists[start: stop]
    i = 0
    for dentist in dentists_temp:
        text1 = f"<b>{str_obj[language]['result_template'][0].upper()}{str(count + 1)}</b>   🦷 🦷 🦷 🦷 🦷\n\n"
        text1 += f"{dentist['service_name']} ({price_splitter(str(dentist['price']))} {str_obj[language]['currency']})\n"
        text1 += f"<b>{dentist['name']}</b>\n"
        text1 += f"<a href =\"{dentist['tg_href']}\">{dentist['fullname']}</a>\n"
        text1 += f"<b>{str_obj[language]['result_template'][9]}:</b> {dentist['worktime']}\n"
        lat = float(dentist["latitude"])
        long = float(dentist["longitude"])
        loc = (lat, long)
        temp = f"({str(oscilate(round(distance(location, loc).kilometers, 2)))} {str_obj[language]['result_template'][7]})" if len(User.objects.filter(tg_user_id=message.chat.id)) != 0 else ""
        text1 += f"{dentist['address']} {temp}.  <a href=\"https://maps.google.com/maps?q={str(lat)},{str(long)}&ll={str(lat)},{str(long)}&z=16\">🗺 {str_obj[language]['result_template'][13]}</a>\n"
        text1 += f"{dentist['phone_number']}\n\n\n"
        count += 1
        i += 1
        text.append(text1)
    text.append("@MyDentistUzBot")
    return "".join(text)


@bot.message_handler(commands=["start"])
def register(message):

    global language
    global status

    if len(User.objects.filter(tg_user_id=message.chat.id)) == 0:
        register_checker(message)
    else:
        user = User.objects.get(tg_user_id=message.chat.id)
        status = "mainmenu"
        user.status = status
        user.save()
        if language == '':
            language = user.language.name
        bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))
