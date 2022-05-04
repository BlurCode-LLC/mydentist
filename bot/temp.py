import telebot
import json
import random
import keypad
from geopy.distance import distance


bot = telebot.TeleBot(config.TOKEN)
db = sql.SQLer()
with open("string_file.json", "r", encoding="utf-8") as file:
    str_obj = json.load(file)


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
        new_price += price[0: 1]
        i += 1
    elif len(price) % 3 == 2:
        new_price += price[0: 2]
        i += 2
    while i != len(price):
        if new_price == "":
            new_price += price[i: (i + 3)]
        else:
            new_price += f" {price[i: (i + 3)]}"
        i += 3
    return new_price


def oscilate(distance):
    return round(distance + random.randrange(500, 2000, 10) / 1000, 2)


def register_checker(message):
    """Use this function to register user in case user is not in the database"""
    db.add_user(message.chat.id, message.chat.first_name,
                message.chat.last_name)
    language = "uz"
    status = "start"
    bot.send_message(message.chat.id, "Tilni tanlang:\nВыберите язык:", reply_markup=keypad.reply_buttons(language, message.chat.id, status))


def sort_by_distance(user, dentists):
    """Use this function to sort the array of dentists by distance"""
    if len(dentists) < 2:
        return dentists
    else:
        pivot = dentists[0]
        less = [i for i in dentists[1:] if distance((i["latitude"], i["longitude"]), (user["latitude"], user["longitude"])).kilometers <= distance(
            (pivot["latitude"], pivot["longitude"]), (user["latitude"], user["longitude"])).kilometers]
        greater = [i for i in dentists[1:] if distance((i["latitude"], i["longitude"]), (user["latitude"], user["longitude"])).kilometers > distance(
            (pivot["latitude"], pivot["longitude"]), (user["latitude"], user["longitude"])).kilometers]
        return sort_by_distance(user, less) + [pivot] + sort_by_distance(user, greater)


def dentists_by_location(language, location, dentists, page=1):
    """Returns dentists by the nearest"""
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


def dentists_by_price(language, message, location, dentists, page=1):
    """Returns dentists by the nearest"""
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
        temp = f"({str(oscilate(round(distance(location, loc).kilometers, 2)))} {str_obj[language]['result_template'][7]})" if db.location_exists(message.chat.id) else ""
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

    if (not db.user_exists(message.chat.id)):
        register_checker(message)
    elif language == '':
        language = db.get_language(message.chat.id)
        status = "mainmenu"
        db.update_status(message.chat.id, status)
        bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons(
            language, message.chat.id, status))
    else:
        status = "mainmenu"
        db.update_status(message.chat.id, status)
        bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons(
            language, message.chat.id, status))


@bot.message_handler(commands=["developers"])
def developers(message):

    global language
    global status

    if (not db.user_exists(message.chat.id)):
        register_checker(message)
    elif language == '':
        language = db.get_language(message.chat.id)
        status = "developers"
        db.update_status(message.chat.id, status)
        bot.send_message(message.chat.id, str_obj[language]["developer_message"], reply_markup=keypad.reply_buttons(
            language, message.chat.id, status), parse_mode="HTML")
    else:
        status = "developers"
        db.update_status(message.chat.id, status)
        bot.send_message(message.chat.id, str_obj[language]["developer_message"], reply_markup=keypad.reply_buttons(
            language, message.chat.id, status), parse_mode="HTML")


@bot.message_handler()
def msg_handler(message):

    global language
    global status
    global page

    if (not db.user_exists(message.chat.id)):
        register_checker(message)
    else:
        if language == "":
            language = db.get_language(message.chat.id)
        if status == "":
            status = db.get_status(message.chat.id)

        if message.text == str_obj[language]["mainmenu_keypad"][0]:
            status = "near1" if (not db.location_exists(
                message.chat.id)) else "near2"
            db.update_status(message.chat.id, status)
            bot.send_message(message.chat.id, str_obj[language]["near_message"], reply_markup=keypad.reply_buttons(
                language, message.chat.id, status))

        elif message.text == str_obj[language]["old_location"]:
            status = "near"
            db.update_status(message.chat.id, status)
            page = 1
            db.update_current_page(message.chat.id, page)
            bot.send_message(message.chat.id, dentists_by_location(language, db.get_location(message.chat.id), sort_by_distance(db.get_location(message.chat.id), db.get_near_dentists(
                language))), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)

        elif message.text == str_obj[language]["mainmenu_keypad"][1]:
            status = "services_big"
            db.update_status(message.chat.id, status)
            bot.send_message(message.chat.id, str_obj[language]["services_big_message"], reply_markup=keypad.reply_buttons(
                language, message.chat.id, status))

        elif message.text in db.get_services_big(language):
            status = message.text
            db.update_status(message.chat.id, status)
            if len(db.get_services_mini(status, language)) > 1:
                bot.send_message(message.chat.id, str_obj[language]["services_mini_message"], reply_markup=keypad.reply_buttons(
                    language, message.chat.id, status))
            else:
                page = 1
                db.update_current_page(message.chat.id, page)
                bot.send_message(message.chat.id, dentists_by_price(language, message, db.get_location(message.chat.id), db.get_dentists_by_price(
                    status, language)), reply_markup=keypad.reply_buttons(language, message.chat.id, message.text, page), parse_mode="HTML", disable_web_page_preview=True)

        elif message.text in db.get_services_mini_all(language):
            status = message.text
            db.update_status(message.chat.id, status)
            page = 1
            db.update_current_page(message.chat.id, page)
            bot.send_message(message.chat.id, dentists_by_price(language, message, db.get_location(message.chat.id), db.get_dentists_by_price(
                status, language)), reply_markup=keypad.reply_buttons(language, message.chat.id, message.text, page), parse_mode="HTML", disable_web_page_preview=True)

        elif message.text == str_obj[language]["mainmenu_keypad"][2]:
            status = "24/7"
            db.update_status(message.chat.id, status)
            page = 1
            db.update_current_page(message.chat.id, page)
            bot.send_message(message.chat.id, dentists_by_location(language, db.get_location(message.chat.id), sort_by_distance(db.get_location(message.chat.id), db.get_24_7_dentists(language))), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)

        elif message.text == str_obj[language]["mainmenu_keypad"][3]:
            status = "about"
            db.update_status(message.chat.id, status)
            bot.send_message(message.chat.id, str_obj[language]["about_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))

        elif message.text == str_obj[language]["mainmenu_keypad"][4]:
            status = "call"
            db.update_status(message.chat.id, status)
            bot.send_message(message.chat.id, str_obj[language]["call_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status))

        elif message.text == "O'z 🇺🇿":
            if language != "uz":
                db.update_language( message.chat.id, "uz" )
                language = "uz"
            bot.send_message( message.chat.id, str_obj[language]["mainmenu_message"], reply_markup = keypad.reply_buttons( "uz", message.chat.id, "mainmenu" ) )

        elif message.text == "Рус 🇷🇺":
            if language != "ru":
                db.update_language( message.chat.id, "ru" )
                language = "ru"
            bot.send_message( message.chat.id, str_obj[language]["mainmenu_message"], reply_markup = keypad.reply_buttons( "ru", message.chat.id, "mainmenu" ) )

        elif message.text == "O'z 🇺🇿 / Рус 🇷🇺":
            if language == "ru":
                db.update_language(message.chat.id, "uz")
                language = "uz"
                bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons("uz", message.chat.id, "mainmenu"))
            elif language == "uz":
                db.update_language(message.chat.id, "ru")
                language = "ru"
                bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons("ru", message.chat.id, "mainmenu"))

        elif message.text == str_obj[language]["mainmenu_keypad"][5]:
            status = "website"
            db.update_status(message.chat.id, status)
            bot.send_message(message.chat.id, str_obj[language]["website_message"], reply_markup=keypad.reply_buttons(language, message.chat.id, status), parse_mode="HTML")

        elif message.text == str_obj[language]["previous_button"]:
            if page == 0:
                page = db.get_current_page(message.chat.id)
            page -= 1
            db.update_current_page(message.chat.id, page)
            if status == "near":
                bot.send_message(message.chat.id, dentists_by_location(language, db.get_location(message.chat.id), sort_by_distance(db.get_location(message.chat.id), db.get_near_dentists(
                    language)), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
            elif status in db.get_services_mini_all(language):
                bot.send_message(message.chat.id, dentists_by_price(language, message, db.get_location(message.chat.id), db.get_dentists_by_price(
                    status, language), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
            elif status == "24/7":
                bot.send_message(message.chat.id, dentists_by_location(language, db.get_location(message.chat.id), sort_by_distance(db.get_location(message.chat.id), db.get_24_7_dentists(
                    language)), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)

        elif message.text == str_obj[language]["next_button"]:
            if page == 0:
                page = db.get_current_page(message.chat.id)
            page += 1
            db.update_current_page(message.chat.id, page)
            if status == "near":
                bot.send_message(message.chat.id, dentists_by_location(language, db.get_location(message.chat.id), sort_by_distance(db.get_location(message.chat.id), db.get_near_dentists(
                    language)), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
            elif status in db.get_services_mini_all(language):
                bot.send_message(message.chat.id, dentists_by_price(language, message, db.get_location(message.chat.id), db.get_dentists_by_price(
                    status, language), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)
            elif status == "24/7":
                bot.send_message(message.chat.id, dentists_by_location(language, db.get_location(message.chat.id), sort_by_distance(db.get_location(message.chat.id), db.get_24_7_dentists(
                    language)), page), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)

        elif message.text == str_obj[language]["back_button"]:
            status = db.get_status(message.chat.id)
            db.update_current_page(message.chat.id, 0)
            if status == "near":
                status = "near1" if (not db.location_exists(
                    message.chat.id)) else "near2"
                db.update_status(message.chat.id, status)
                bot.send_message(message.chat.id, str_obj[language]["near_message"], reply_markup=keypad.reply_buttons(
                    language, message.chat.id, "near1" if (not db.location_exists(message.chat.id)) else "near2"))
            elif status in db.get_services_big(language):
                status = "services_big"
                db.update_status(message.chat.id, status)
                bot.send_message(message.chat.id, str_obj[language]["services_big_message"], reply_markup=keypad.reply_buttons(
                    language, message.chat.id, "services_big"))
            elif status in db.get_services_mini_all(language):
                if status == db.get_services_mini_reverse(status, language):
                    status = "services_big"
                    db.update_status(message.chat.id, status)
                    bot.send_message(message.chat.id, str_obj[language]["services_big_message"], reply_markup=keypad.reply_buttons(
                        language, message.chat.id, "services_big"))
                else:
                    status = db.get_services_mini_reverse(status, language)
                    db.update_status(message.chat.id, status)
                    bot.send_message(message.chat.id, str_obj[language]["services_mini_message"], reply_markup=keypad.reply_buttons(
                        language, message.chat.id, status))
            elif status in ["about", "call", "comment"]:
                status = "MyDentist"
                db.update_status(message.chat.id, status)
                bot.send_message(message.chat.id, str_obj[language]["mydentist_message"], reply_markup=keypad.reply_buttons(
                    language, message.chat.id, status))

        elif message.text == str_obj[language]["mainmenu_button"]:
            status = "mainmenu"
            db.update_status(message.chat.id, status)
            db.update_current_page(message.chat.id, 0)
            bot.send_message(message.chat.id, str_obj[language]["mainmenu_message"], reply_markup=keypad.reply_buttons(
                language, message.chat.id, "mainmenu"))


@bot.message_handler(content_types=["location"])
def handle_location(message):
    if (not db.location_exists(message.chat.id)):
        db.add_location(message.chat.id, message.location.latitude,
                        message.location.longitude)
    else:
        db.update_location(
            message.chat.id, message.location.latitude, message.location.longitude)
    status = "near"
    db.update_status(message.chat.id, status)
    page = 1
    db.update_current_page(message.chat.id, page)
    bot.send_message(message.chat.id, dentists_by_location(language, db.get_location(message.chat.id), sort_by_distance(db.get_location(message.chat.id), db.get_near_dentists(
        language))), reply_markup=keypad.reply_buttons(language, message.chat.id, status, page), parse_mode="HTML", disable_web_page_preview=True)


if __name__ == "__main__":
    bot.polling(True)
