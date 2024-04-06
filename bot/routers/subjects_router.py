from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import future_api
from bot.keyboards import keyboard_go_to_menu, keyboard_for_subject
from bot.states import AFKState, SubjectState

subjects_router = Router()


@subjects_router.message(SubjectState.chosen_subject, F.text == 'К списку предметов')
@subjects_router.message(SubjectState.lecture_opened, F.text == 'К списку предметов')
@subjects_router.message(SubjectState.choosing_lecture, F.text == 'К списку предметов')
@subjects_router.message(AFKState.logged, F.text == "Мои предметы 🥐")
async def my_subjects_button(message: types.Message, state: FSMContext):
    subjects = await future_api.get_info_about_subject_db(message.from_user.id)
    keyboard = [[]]
    for subject in subjects:
        if len(keyboard[-1]) < 2:
            keyboard[-1].append(types.InlineKeyboardButton(
                text=f"{subject[1]}",
                callback_data=f"{subject[0]}")
            )
        else:
            keyboard.append([types.InlineKeyboardButton(
                text=f"{subject[1]}",
                callback_data=f"{subject[0]}")]
            )
    builder = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.reply('Доступные предметы: ', reply_markup=builder)
    await state.set_state(SubjectState.choosing_subject)
    state_data = await state.get_data()
    if 'subject_id' in state_data.keys():
        del state_data['subject_id']
        await state.set_data(state_data)


@subjects_router.message(SubjectState.choosing_subject, F.text.isdigit())
async def my_subjects_button(message: types.Message, state: FSMContext):
    try:
        subject = await future_api.get_info_about_subject(message.from_user.id, int(message.text))
        content = Text(
            'Предмет ',
            Bold(subject[1]),
            '\nПреподаватель: ',
            Bold(subject[2]),
            '\nУспеваемость: ',
            Bold(subject[3]),
            '\nТекущая лекция: ',
            Bold(subject[4]),
        )
        await message.answer(**content.as_kwargs(), reply_markup=keyboard_for_subject())
        await state.set_state(SubjectState.chosen_subject)
        await state.set_data({'subject_id': subject[0]})
    except ValueError as e:
        await message.answer(f'{e}')


@subjects_router.message(SubjectState.choosing_subject)
async def my_subjects_button(message: types.Message):
    await message.reply('В номере предмета должны быть только цифры')
