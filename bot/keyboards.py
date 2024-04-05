from aiogram import types


def keyboard_for_menu():
    kb = [
        [types.KeyboardButton(text="Мой профиль 🍕"),
         types.KeyboardButton(text="Мои предметы 🥐")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def keyboard_go_to_menu():
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def keyboard_for_subject():
    kb = [
        [types.KeyboardButton(text="В меню"),
         types.KeyboardButton(text="К списку предметов")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard