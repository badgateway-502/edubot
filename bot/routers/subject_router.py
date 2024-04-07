from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot import future_api
from bot.keyboards import keyboard_for_current_lecture, keyboard_for_all_lectures, keyboard_for_old_lecture
from bot.states import SubjectState, Quiz, Lab

subject_router = Router()


@subject_router.message(SubjectState.chosen_subject, F.text == "Список всех доступных лекций")
@subject_router.message(SubjectState.lecture_opened, F.text == "Список всех доступных лекций")
async def list_of_available_lectures(message: types.Message, state: FSMContext):
    # получаем информацию о доступных лекциях
    lecture_list = future_api.get_lectures_all_db((await state.get_data())['subject_id'])
    text = 'Доступные лекции: '
    for lecture in lecture_list:  # проходимся по списку лекций и выводим все доступные лекции
        text += f'\n {lecture["id"]} {lecture["title"]}'
    text += '\n\n чтобы просмотреть лекцию, пожалуйста выберите её номер'
    await message.answer(text, reply_markup=keyboard_for_all_lectures())
    await state.set_state(SubjectState.choosing_lecture)
    state_data = await state.get_data()
    if 'lecture_id' in state_data.keys():  # удаляем номер лекции если он лежит в state
        del state_data['lecture_id']
        await state.set_data(state_data)


@subject_router.message(SubjectState.choosing_lecture, F.text.isdigit())
@subject_router.message(Quiz.finished_quiz, F.text == 'Вернуться к лекции')
@subject_router.message(Quiz.scalare_question, F.text == 'Обратно к лекции')
@subject_router.message(Quiz.variants_question, F.text == 'Обратно к лекции')
@subject_router.message(Lab.lab_opened, F.text == 'К лекции')
async def some_lecture(message: types.Message, state: FSMContext):
    # выводим все что есть для данной лекции
    # если есть видео - выводим
    # если есть файл лекции - выводим
    # если есть текст лекции - выводим
    # выводим лекцию которую ученик уже прошел

    try:
        idlect = message.text
        if 'lecture_id' in (await state.get_data()).keys():
            idlect = (await state.get_data())['lecture_id']
        cur_lecture = future_api.get_lecture_by_number((await state.get_data())['subject_id'], int(idlect))
        print('help23')
        keyboard = keyboard_for_current_lecture(cur_lecture['test'], cur_lecture["lab"])
        if cur_lecture['video_file_id']:
            await message.answer_video(cur_lecture['video_file_id'], reply_markup=keyboard)
        if cur_lecture['description_file_id']:
            await message.answer_document(cur_lecture['description_file_id'], reply_markup=keyboard)
        if cur_lecture['text_description']:
            await message.answer(cur_lecture['text_description'], reply_markup=keyboard)
        print('help3')
        await state.set_state(SubjectState.lecture_opened)
        state_data = await state.get_data()
        state_data['lecture_id'] = cur_lecture['id']
        await state.set_data(state_data)
        print('help')
    except ValueError as e:
        await message.answer(f'{e}')
