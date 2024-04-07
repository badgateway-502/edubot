from typing import List

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

from bot.entity_types import SubjectType

# клавиатура с меню и предметами
def keyboard_for_menu() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="Мой профиль 🍕"),
         types.KeyboardButton(text="Мои предметы 🥐")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

# клавиатура в меню - используется в профиле
def keyboard_go_to_menu() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

# клавиатура предметов
def keyboard_subjects(subjects: List[SubjectType]) -> ReplyKeyboardMarkup:
    keyboard = [[]]
    for subject in subjects:
        if len(keyboard[-1]) < 2:
            keyboard[-1].append(types.KeyboardButton(
                text=f"{subject['name']}",
            ))
        else:
            keyboard.append([types.KeyboardButton(
                text=f"{subject['name']}",
            )])
    keyboard.append([types.KeyboardButton(text="В меню", callback_data="В меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard)

# клавиатура для выбранного предмета
def keyboard_for_subject() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="Текущая лекция"),
         types.KeyboardButton(text="Список всех доступных лекций")],
        [types.KeyboardButton(text="В меню"),
         types.KeyboardButton(text="К списку предметов")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

# клавиатура для выбранной лекции
def keyboard_for_lecture() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="В меню"),
         types.KeyboardButton(text="К списку предметов"),
         types.KeyboardButton(text="Список всех доступных лекций"),
         types.KeyboardButton(text="Пройти тест")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

# клавиатура для списка лекций
def keyboard_for_all_lectures() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="В меню"),
         types.KeyboardButton(text="К списку предметов"),
         types.KeyboardButton(text="Текущая лекция")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


# если вопрос первый, то отдаем пользователю кнопки "в меню" и ">"
# если вопрос последний, то отдаем пользователю кнопки "<" и "в меню"
# если вопрос единственный (тоесть первый и последний), то отдаем пользователю кнопку "в меню"
# клавиатура в тесте
def keyboard_quiz(first: bool = False, last: bool = False, first_and_last: bool = False) -> ReplyKeyboardMarkup:
    if first:
        kb = [
            [
                types.KeyboardButton(text="В меню"),
                types.KeyboardButton(text=">"),
            ],
        ]
    elif last:
        kb = [
            [
                types.KeyboardButton(text="<"),
                types.KeyboardButton(text="В меню"),
            ],
        ]
    elif first_and_last:
        kb = [
            [
                types.KeyboardButton(text="В меню"),
            ],
        ]
    else:
        kb = [
            [
                types.KeyboardButton(text="<"),
                types.KeyboardButton(text="В меню"),
                types.KeyboardButton(text=">")
            ],
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

# инлайн клавиатура для выбора предметов
def keyboard_answer_variants(variants: List[str]) -> types.InlineKeyboardMarkup:
    keyboard = [[]]
    for variant in variants:
        if len(keyboard[-1]) < 3:
            keyboard[-1].append(types.InlineKeyboardButton(
                text=f"{variant}",
            ))
        else:
            keyboard.append([types.InlineKeyboardButton(
                text=f"{variant}",
            )])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard
