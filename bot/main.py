import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold

from config_reader import config
from aiogram import F

from dataclasses import dataclass

TOKEN_KEY = '7172148895:AAHBcVjYuhiykWF9nt6uqGMbvn2eERj9dpQ'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher()


@dataclass
class Student:
    id: int
    name: str
    surname: str
    academic_performance: dict

    def get_info(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'academic_performance': self.academic_performance
        }


async def check_user_db():
    is_in_db = True
    return is_in_db


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if await check_user_db():
        kb = [
            [types.KeyboardButton(text="Мой профиль 🍕"),
             types.KeyboardButton(text="Мои предметы 🥐")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
        await message.answer("Меню", reply_markup=keyboard)
    else:
        await message.answer("you need to register")


async def get_academic_performance_of_current_subject_db(subject: str, user_id: int):
    if user_id == 840307055:
        if subject == 'math':
            return 100
        if subject == 'english':
            return 100
        if subject == 'chemistry':
            return 100
        if subject == 'programming':
            return 100
        if subject == 'history':
            return 100


async def get_whole_score_of_current_subject_db(subject):
    if subject == 'math':
        return 120
    if subject == 'english':
        return 120
    if subject == 'chemistry':
        return 120
    if subject == 'programming':
        return 120
    if subject == 'history':
        return 120


async def get_available_subjects_db():
    dicto = ['math', 'english', 'chemistry', 'programming', 'history']
    return dicto


async def get_info_user_db(user_id: int):
    available_subjects = await get_available_subjects_db()
    academic_performance = {}
    for subject in available_subjects:
        academic_performance[subject] = await get_academic_performance_of_current_subject_db(subject, user_id) / (
            await get_whole_score_of_current_subject_db(subject)) * 100

    dicto = {
        'id': 840307055,
        'name': 'Кирилл',
        'surname': 'Подковырин',
        'academic_performance': academic_performance
    }
    return dicto


async def get_info_about_user(user_id: int):
    return await get_info_user_db(user_id)


@dp.message(F.text == "Мой профиль 🍕")
async def my_profile_button(message: types.Message):
    user = await get_info_about_user(message.from_user.id)
    student = Student(**user)
    info_student = student.get_info()

    academic_performance = []
    for subject in info_student['academic_performance'].items():
        text = f'\n{subject[0]}: {subject[1]:02}%'
        academic_performance.append(text)

    content = Text(
        'Профиль ',
        Bold(info_student['name']),
        ' ',
        Bold(info_student['surname']),
        '\nУспеваемость:',
        *academic_performance
    )

    await message.reply(**content.as_kwargs(), reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text == "Мои предметы 🥐")
async def my_subjects_button(message: types.Message):
    await message.reply("math info english", reply_markup=types.ReplyKeyboardRemove())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
