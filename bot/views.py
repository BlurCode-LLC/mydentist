import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.distance import distance
from json import loads
from random import randrange
from telebot import TeleBot, types
from baseapp.models import Language

from dentist.models import Service_category_translation, Service_translation

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
    return distance
    # return round(distance + randrange(500, 2000, 10) / 1000, 2)


def register_checker(message):
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


def dentists_by_location(language, location, dentists, page=1):
    location = (location['latitude'], location['longitude'])
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
        text1 += f"<b>{dentist['clinic_name']}</b>\n"
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


def dentists_by_price(language, message, location, dentists, page=1):
    location = (location['latitude'], location['longitude'])
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
        text1 += f"<b>{dentist['clinic_name']}</b>\n"
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

    try:
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
    except Exception as E:
        with open("debug.txt", "a") as file:
            file.write(str(E))


@bot.message_handler(commands=["developers"])
def developers(message):

    global language
    global status

    try:
        if len(User.objects.filter(tg_user_id=message.chat.id)) == 0:
            register_checker(message)
        user = User.objects.get(tg_user_id=message.chat.id)
        status = "developers"
        user.status = status
        user.save()
        if language == '':
            language = user.language.name
        bot.send_message(message.chat.id, str_obj[language]["developer_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status), parse_mode="HTML")
    except Exception as E:
        with open("debug.txt", "a") as file:
            file.write(str(E))


@bot.message_handler()
def msg_handler(message):

    global language
    global status
    global page

    try:
        if len(User.objects.filter(tg_user_id=message.chat.id)) == 0:
            register_checker(message)
        else:
            user = User.objects.get(tg_user_id=message.chat.id)
            if language == "":
                language = user.language.name
            if status == "":
                status = user.status

            if message.text == str_obj[language]["mainmenu_keypad"][0]:
                status = "near1" if location_not_exists(user) else "near2"
                user.status = status
                user.save()
                bot.send_message(message.chat.id, str_obj[language]["near_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))

            elif message.text == str_obj[language]["old_location"]:
                status = "near"
                page = 1
                user.status = status
                user.current_page = page
                user.save()
                location = get_location(user)
                bot.send_message(message.chat.id, dentists_by_location(language, location, sort_by_distance(location, get_near_dentists(language, str_obj[language]["24_hour"]))), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)

            elif message.text == str_obj[language]["mainmenu_keypad"][1]:
                status = "services"
                user.status = status
                user.save()
                bot.send_message(message.chat.id, f"{str_obj[language]['services_big_message']}\n\n{str_obj[language]['services_mini_message']}", reply_markup=keypad.reply_buttons(language, message.chat.id, status))

            elif message.text in get_categories(language):
                status = message.text
                user.status = status
                user.save()
                services = Service_category_translation.objects.filter(name=status).first()
                if services is not None:
                    services = services.service_category.service_category_service.distinct("name")
                    if len(services) > 1:
                        bot.send_message(message.chat.id, str_obj[language]["services_mini_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))
                    else:
                        page = 1
                        user.current_page = page
                        user.save()
                        location = get_location(user)
                        bot.send_message(message.chat.id, dentists_by_price(language, message, location, get_dentists_by_price(status, language, str_obj[language]["24_hour"])), reply_markup=keypad.reply_buttons(language, message.chat.id, message.text, page), parse_mode="HTML", disable_web_page_preview=True)

            elif message.text in get_services_all(language):
                status = message.text
                page = 1
                user.status = status
                user.current_page = page
                user.save()
                bot.send_message(message.chat.id, dentists_by_price(language, message, get_location(user), get_dentists_by_price(status, language, str_obj[language]["24_hour"])), reply_markup=keypad.reply_buttons(language, message.chat.id, message.text, page), parse_mode="HTML", disable_web_page_preview=True)

            elif message.text == str_obj[language]["mainmenu_keypad"][2]:
                status = "24/7"
                page = 1
                user.status = status
                user.current_page = page
                user.save()
                bot.send_message(message.chat.id, dentists_by_location(language, get_location(user), sort_by_distance(get_location(user), get_24_7_dentists(language, str_obj[language]["24_hour"]))), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
                

            elif message.text == str_obj[language]["mainmenu_keypad"][3]:
                status = "about"
                user.status = status
                user.save()
                bot.send_message(message.chat.id, str_obj[language]["about_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))

            elif message.text == str_obj[language]["mainmenu_keypad"][4]:
                status = "call"
                user.status = status
                user.save()
                bot.send_message(message.chat.id, str_obj[language]["call_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))

            elif message.text == "O'z 🇺🇿":
                if language != "uz":
                    language = "uz"
                    user.language_id = Language.objects.get(name=language).id
                    user.save()
                bot.send_message( message.chat.id, str_obj[language]["mainmenu_message"], reply_markup = keypad.reply_buttons( "uz", message.chat.id, "mainmenu" ) )

            elif message.text == "Рус 🇷🇺":
                if language != "ru":
                    language = "ru"
                    user.language_id = Language.objects.get(name=language).id
                    user.save()
                bot.send_message( message.chat.id, str_obj[language]["mainmenu_message"], reply_markup = keypad.reply_buttons( "ru", message.chat.id, "mainmenu" ) )

            elif message.text == "O'z 🇺🇿 / Рус 🇷🇺":
                if language == "ru":
                    language = "uz"
                elif language == "uz":
                    language = "ru"
                user.language_id = Language.objects.get(name=language).id
                user.save()
                bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, "mainmenu"))

            elif message.text == str_obj[language]["mainmenu_keypad"][5]:
                status = "website"
                user.status = status
                user.save()
                bot.send_message(message.chat.id, str_obj[language]["website_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status), parse_mode="HTML")

            elif message.text == str_obj[language]["previous_button"]:
                if page == 0:
                    page = user.current_page
                page -= 1
                user.current_page = page
                user.save()
                if status == "near":
                    bot.send_message(message.chat.id, dentists_by_location(language, get_location(user), sort_by_distance(get_location(user), get_near_dentists(language, str_obj[language]["24_hour"])), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
                elif status in get_services_all(language):
                    bot.send_message(message.chat.id, dentists_by_price(language, message, get_location(user), get_dentists_by_price(status, language, str_obj[language]["24_hour"]), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
                elif status == "24/7":
                    bot.send_message(message.chat.id, dentists_by_location(language, get_location(user), sort_by_distance(get_location(user), get_24_7_dentists(language, str_obj[language]["24_hour"])), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)

            elif message.text == str_obj[language]["next_button"]:
                if page == 0:
                    page = user.current_page
                page += 1
                user.current_page = page
                user.save()
                if status == "near":
                    bot.send_message(message.chat.id, dentists_by_location(language, get_location(user), sort_by_distance(get_location(user), get_near_dentists(language, str_obj[language]["24_hour"])), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
                elif status in get_services_all(language):
                    bot.send_message(message.chat.id, dentists_by_price(language, message, get_location(user), get_dentists_by_price(status, language, str_obj[language]["24_hour"]), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
                elif status == "24/7":
                    bot.send_message(message.chat.id, dentists_by_location(language, get_location(user), sort_by_distance(get_location(user), get_24_7_dentists(language, str_obj[language]["24_hour"])), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)

            elif message.text == str_obj[language]["back_button"]:
                status = user.status
                user.current_page = 0
                if status == "near":
                    status = "near1" if location_not_exists(user) else "near2"
                    user.status = status
                    user.save()
                    bot.send_message(message.chat.id, str_obj[language]["near_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, "near1" if location_not_exists(user) else "near2"))
                elif status in get_categories(language):
                    status = "services"
                    user.status = status
                    user.save()
                    bot.send_message(message.chat.id, str_obj[language]["services_big_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))
                elif status in get_services_all(language):
                    if status == get_category(status, language):
                        status = "services"
                        user.status = status
                        user.save()
                        bot.send_message(message.chat.id, str_obj[language]["services_big_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))
                    else:
                        status = get_category(status, language)
                        user.status = status
                        user.save()
                        bot.send_message(message.chat.id, str_obj[language]["services_mini_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))
                elif status in ["about", "call", "comment"]:
                    status = "MyDentist"
                    user.status = status
                    user.save()
                    bot.send_message(message.chat.id, str_obj[language]["mydentist_message"], reply_markup=keypad.reply_buttons(
                        language, message.chat.id, status))

            elif message.text == str_obj[language]["mainmenu_button"]:
                status = "mainmenu"
                user.status = status
                user.current_page = 0
                user.save()
                bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, "mainmenu"))
    except Exception as E:
        with open("debug.txt", "a") as file:
            file.write(str(E))


@bot.message_handler(content_types=["location"])
def handle_location(message):

    global language
    global status
    global page

    try:
        if len(User.objects.filter(tg_user_id=message.chat.id)) == 0:
            register_checker(message)
        else:
            user = User.objects.get(tg_user_id=message.chat.id)
            if language == "":
                language = user.language.name
            if status == "":
                status = user.status

        user = User.objects.get(tg_user_id=message.chat.id)
        user.latitude = message.location.latitude
        user.longitude = message.location.longitude
        user.save()
        status = "near"
        page = 1
        user.status = status
        user.current_page = page
        user.save()
        bot.send_message(message.chat.id, dentists_by_location(language, get_location(user), sort_by_distance(get_location(user), get_near_dentists(language, str_obj[language]["24_hour"]))), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
    except Exception as E:
        with open("debug.txt", "a") as file:
            file.write(str(E))
