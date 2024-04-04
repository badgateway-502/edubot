import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Bold

from future_api import get_info_user_db, check_user_db, create_new_student

import validate
from states import SignInState, AFKState
from entities import Student

from config_reader import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


def keyboard_for_menu():
    kb = [
        [types.KeyboardButton(text="Мой профиль 🍕"),
         types.KeyboardButton(text="Мои предметы 🥐")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if await check_user_db(message.from_user.id):
        await message.answer("Меню", reply_markup=keyboard_for_menu())
        await state.set_state(AFKState.logged)
    else:
        await message.answer("Пожалуйста, зарегестрируйтесь. Введите ваше имя и фамилию.")
        await state.set_state(SignInState.signing_in)


@dp.message(SignInState.signing_in)
async def signing_in(message: types.Message, state: FSMContext):
    try:
        if validate.validate_name(message.text):
            name = message.text.split()
            await create_new_student(name[0], name[1], message.from_user.id)
            await message.answer("Меню", reply_markup=keyboard_for_menu())
            await state.set_state(AFKState.logged)
    except ValueError as e:
        await message.answer(f'{e}')


@dp.message(AFKState.logged, Command("menu"))
async def menu(message: types.Message):
    await message.answer("Меню", reply_markup=keyboard_for_menu())


async def get_info_about_user(user_id: int):
    return await get_info_user_db(user_id)


@dp.message(F.text == "Мой профиль 🍕")
async def my_profile_button(message: types.Message):
    user = await get_info_about_user(message.from_user.id)
    student = Student(**user)

    academic_performance = []
    for subject in student.academic_performance.items():
        text = f'\n{subject[0]}: {subject[1]:02}%'
        academic_performance.append(text)

    content = Text(
        'Профиль ',
        Bold(student.name),
        ' ',
        Bold(student.surname),
        '\nУспеваемость:',
        *academic_performance
    )

    await message.reply(**content.as_kwargs(), reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text == "Мои предметы 🥐")
async def my_subjects_button(message: types.Message):
    await message.reply(message.chat.type, reply_markup=types.ReplyKeyboardRemove())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
