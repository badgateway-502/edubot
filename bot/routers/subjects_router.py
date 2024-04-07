from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Bold

from bot import future_api
from bot.keyboards import keyboard_for_subject, keyboard_subjects
from bot.states import AFKState, SubjectState

subjects_router = Router()


@subjects_router.message(AFKState.logged, F.text == "Мои предметы 🥐")
@subjects_router.message(SubjectState.choosing_subject, F.text == 'К списку предметов')
@subjects_router.message(SubjectState.chosen_subject, F.text == 'К списку предметов')
@subjects_router.message(SubjectState.choosing_lecture, F.text == 'К списку предметов')
@subjects_router.message(SubjectState.lecture_opened, F.text == 'К списку предметов')
async def my_subjects_button(message: types.Message, state: FSMContext):
    # получаем информацию о всех предметах
    subjects = future_api.get_info_about_subjects_db()
    keyboard = keyboard_subjects(subjects)  # из keyboard_subjects получаем клавиатуру, которая знает все предметы
    await message.reply('Доступные предметы: ', reply_markup=keyboard)
    await state.set_state(SubjectState.choosing_subject)
    state_data = await state.get_data()  # удаляем информацию о выбранном предмете если он когдато был выбран
    if 'subject_id' in state_data.keys():
        del state_data['subject_id']
        await state.set_data(state_data)


@subjects_router.message(SubjectState.choosing_subject, F.text.in_(future_api.get_subjects_titles().keys()))
async def my_subjects_button(message: types.Message, state: FSMContext):
    try:
        subject_id = future_api.get_subjects_titles()[message.text]  # получаем id конкретного предмета по его названию
        subject = future_api.get_info_current_subject(message.from_user.id,
                                                      subject_id)  # получаем всю информацию о предмете
        content = Text(
            'Предмет ',
            Bold(subject['name']),
            '\nПреподаватель: ',
            Bold(subject['teacher']['firstname'] + subject['teacher']['lastname']),
            # '\nУспеваемость: ',
            # Bold(subject[3]),
            # '\nТекущая лекция: ',
            # Bold(subject[4]),
            # TODO
        )
        await message.answer(**content.as_kwargs(), reply_markup=keyboard_for_subject())
        await state.set_state(SubjectState.chosen_subject)
        await state.set_data({'subject_id': subject_id})
    except ValueError as e:
        await message.answer(f'{e}')
