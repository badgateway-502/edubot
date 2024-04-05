from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot import future_api
from bot.keyboards import keyboard_for_lecture, keyboard_for_all_lectures
from bot.states import SubjectState

subject_router = Router()


@subject_router.message(SubjectState.chosen_subject, F.text == "Текущая лекция")
@subject_router.message(SubjectState.choosing_lecture, F.text == "Текущая лекция")
async def my_subjects_button(message: types.Message, state: FSMContext):
    cur_lecture = await future_api.get_current_lecture_db(message.from_user.id, (await state.get_data())['subject_id'])
    if 'video_id' in cur_lecture.keys():
        await message.answer_video(cur_lecture['video_id'], reply_markup=keyboard_for_lecture())
    if 'pdf_id' in cur_lecture.keys():
        await message.answer_document(cur_lecture['pdf_id'], reply_markup=keyboard_for_lecture())
    if 'text' in cur_lecture.keys():
        await message.answer(cur_lecture['text'], reply_markup=keyboard_for_lecture())

    await state.set_state(SubjectState.current_lecture)


@subject_router.message(SubjectState.chosen_subject, F.text == "Список всех доступных лекций")
@subject_router.message(SubjectState.current_lecture, F.text == "Список всех доступных лекций")
@subject_router.message(SubjectState.old_lecture, F.text == "Список всех доступных лекций")
async def my_subjects_button(message: types.Message, state: FSMContext):
    lecture_list = await future_api.get_lectures_all_db(message.from_user.id, (await state.get_data())['subject_id'])
    text = 'Доступные лекции: '
    for lecture in lecture_list:
        text += f'\n {lecture[0]} {lecture[1]}'
    text += '\n\n чтобы просмотреть лекцию, пожалуйста выберите её номер'
    await message.answer(text, reply_markup=keyboard_for_all_lectures())
    await state.set_state(SubjectState.choosing_lecture)


@subject_router.message(SubjectState.choosing_lecture, F.text.isdigit())
async def my_subjects_button(message: types.Message, state: FSMContext):
    try:
        cur_lecture = await future_api.get_lectures_all_db(message.from_user.id, (await state.get_data())['subject_id'],
                                                           int(message.text))
        if 'video_id' in cur_lecture.keys():
            await message.answer_video(cur_lecture['video_id'], reply_markup=keyboard_for_lecture())
        if 'pdf_id' in cur_lecture.keys():
            await message.answer_document(cur_lecture['pdf_id'], reply_markup=keyboard_for_lecture())
        if 'text' in cur_lecture.keys():
            await message.answer(cur_lecture['text'], reply_markup=keyboard_for_lecture())

        await state.set_state(SubjectState.old_lecture)
    except ValueError as e:
        await message.answer(f'{e}', reply_markup=keyboard_for_lecture())


@subject_router.message(SubjectState.choosing_lecture)
async def my_subjects_button(message: types.Message):
    await message.answer('Такого номера не существует')
