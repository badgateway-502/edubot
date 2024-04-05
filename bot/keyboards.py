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
        [types.KeyboardButton(text="Текущая лекция"),
         types.KeyboardButton(text="Список всех доступных лекций")],
        [types.KeyboardButton(text="В меню"),
         types.KeyboardButton(text="К списку предметов")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def keyboard_for_lecture():
    kb = [
        [types.KeyboardButton(text="В меню"),
         types.KeyboardButton(text="К списку предметов"),
         types.KeyboardButton(text="Список всех доступных лекций")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def keyboard_for_all_lectures():
    kb = [
        [types.KeyboardButton(text="В меню"),
         types.KeyboardButton(text="К списку предметов"),
         types.KeyboardButton(text="Текущая лекция")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
