import telebot
from json import load

from .models import User
from .utils import get_near_dentists

with open("bot/string_file.json", "r", encoding="utf-8") as file:
    str_obj = load(file)


def reply_buttons(lang, id, status, page=0):
    """Use this function to send reply keyboards depending on user preferred language and status"""
    if status == "start":
        return telebot.types.ReplyKeyboardMarkup(True, row_width=1).row(
            telebot.types.KeyboardButton("O'z 🇺🇿"),
            telebot.types.KeyboardButton("Рус 🇷🇺")
        )

    elif status == "mainmenu":
        return telebot.types.ReplyKeyboardMarkup(True, row_width=1).add(
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_keypad"][0])
        ).row(
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_keypad"][1]),
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_keypad"][2])
        ).row(
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_keypad"][3]),
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_keypad"][4])
        ).row(
            telebot.types.KeyboardButton("O'z 🇺🇿 / Рус 🇷🇺"),
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_keypad"][5])
        )

    elif status == "near1":
        return telebot.types.ReplyKeyboardMarkup(True, row_width=1).add(
            telebot.types.KeyboardButton(str_obj[lang]["send_location"], request_location=True),
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
        )

    elif status == "near2":
        return telebot.types.ReplyKeyboardMarkup(True, row_width=1).add(
            telebot.types.KeyboardButton(str_obj[lang]["update_location"], request_location=True),
            telebot.types.KeyboardButton(str_obj[lang]["old_location"]),
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
        )

    elif status == "near":
        keyboard = telebot.types.ReplyKeyboardMarkup(True, row_width=1)
        near_dentists = get_near_dentists(lang, str_obj[lang]["24_hour"])
        if len(near_dentists) > 4:
            if page * 4 >= len(near_dentists):
                keyboard.row(
                    telebot.types.KeyboardButton(
                        str_obj[lang]["previous_button"])
                )
            elif page == 1:
                keyboard.row(
                    telebot.types.KeyboardButton(str_obj[lang]["next_button"])
                )
            else:
                keyboard.row(
                    telebot.types.KeyboardButton(
                        str_obj[lang]["previous_button"]),
                    telebot.types.KeyboardButton(str_obj[lang]["next_button"])
                )
        return keyboard.add(
            telebot.types.KeyboardButton(str_obj[lang]["back_button"]),
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
        )

    # elif status == "services_big":
    #     keyboard = telebot.types.ReplyKeyboardMarkup(True, row_width=1)
    #     buttons = db.get_services_big(lang)
    #     if len(buttons) % 2 == 0:
    #         for i in range(0, len(buttons), 2):
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(buttons[i]),
    #                 telebot.types.KeyboardButton(buttons[i + 1])
    #             )
    #     else:
    #         for i in range(0, len(buttons) - 1, 2):
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(buttons[i]),
    #                 telebot.types.KeyboardButton(buttons[i + 1])
    #             )
    #         keyboard.row(telebot.types.KeyboardButton(
    #             buttons[len(buttons) - 1]))
    #     return keyboard.row(telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"]))

    # elif status in db.get_services_big(lang) and len(db.get_services_mini(status, lang)) > 1:
    #     keyboard = telebot.types.ReplyKeyboardMarkup(True, row_width=1)
    #     buttons = db.get_services_mini(status, lang)
    #     if len(buttons) % 2 == 0:
    #         for i in range(0, len(buttons), 2):
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(buttons[i]),
    #                 telebot.types.KeyboardButton(buttons[i + 1])
    #             )
    #     else:
    #         for i in range(0, len(buttons) - 1, 2):
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(buttons[i]),
    #                 telebot.types.KeyboardButton(buttons[i + 1])
    #             )
    #         keyboard.row(telebot.types.KeyboardButton(
    #             buttons[len(buttons) - 1]))
    #     return keyboard.add(
    #         telebot.types.KeyboardButton(str_obj[lang]["back_button"]),
    #         telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
    #     )

    # elif status in db.get_services_mini_all(lang):
    #     keyboard = telebot.types.ReplyKeyboardMarkup(True, row_width=1)
    #     if len(db.get_dentists_by_price(status, lang)) > 4:
    #         if page * 4 >= len(db.get_dentists_by_price(status, lang)):
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(
    #                     str_obj[lang]["previous_button"])
    #             )
    #         elif page == 1:
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(str_obj[lang]["next_button"])
    #             )
    #         else:
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(
    #                     str_obj[lang]["previous_button"]),
    #                 telebot.types.KeyboardButton(str_obj[lang]["next_button"])
    #             )
    #     return keyboard.add(
    #         telebot.types.KeyboardButton(str_obj[lang]["back_button"]),
    #         telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
    #     )

    # elif status == "24/7":
    #     keyboard = telebot.types.ReplyKeyboardMarkup(True, row_width=1)
    #     if len(db.get_24_7_dentists(lang)) > 4:
    #         if page * 4 >= len(db.get_24_7_dentists(lang)):
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(
    #                     str_obj[lang]["previous_button"])
    #             )
    #         elif page == 1:
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(str_obj[lang]["next_button"])
    #             )
    #         else:
    #             keyboard.row(
    #                 telebot.types.KeyboardButton(
    #                     str_obj[lang]["previous_button"]),
    #                 telebot.types.KeyboardButton(str_obj[lang]["next_button"])
    #             )
    #     return keyboard.add(
    #         telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
    #     )

    elif status == "about" or status == "call":
        return telebot.types.ReplyKeyboardMarkup(True, row_width=1).add(
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
        )

    elif status == "website":
        return telebot.types.ReplyKeyboardMarkup(True, row_width=1).add(
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
        )

    elif status == "developers":
        return telebot.types.ReplyKeyboardMarkup(True, row_width=1).add(
            telebot.types.KeyboardButton(str_obj[lang]["mainmenu_button"])
        )
