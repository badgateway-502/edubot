from aiogram import Router, F, types
from aiogram.utils.formatting import Text, Bold

from bot import future_api
from bot.entities import Student
from bot.keyboards import keyboard_go_to_menu
from bot.states import AFKState

profile_router = Router()


@profile_router.message(AFKState.logged, F.text == "Мой профиль 🍕")
async def my_profile_button(message: types.Message):
    # выводим информацию о пользователе. ПРОФИЛЬ
    user = future_api.get_info_user_db(message.from_user.id)
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

    await message.reply(**content.as_kwargs(), reply_markup=keyboard_go_to_menu())
