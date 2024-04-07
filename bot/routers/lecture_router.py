from typing import List, Dict

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot import future_api
from bot.keyboards import keyboard_quiz, keyboard_answer_variants
from bot.states import SubjectState
from bot.states import Quiz

lecture_router = Router()


# функция для проверки того на каком вопросе находится ученик и нужно ли менять калвиатуру
def check_questions_len(questions: List, question_id_now: int) -> Dict[str, bool]:
    if len(questions) > 1 and question_id_now == 0:
        return {'first': True}
    elif len(questions) > 1 and question_id_now == len(questions) - 1:
        return {'last': True}
    elif len(questions) == 1:
        return {'first_and_last': True}


@lecture_router.message(SubjectState.lecture_opened, F.text == "Пройти тест")
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lecture = future_api.get_lecture_by_number(state_data['subject_id'], state_data['lecture_id'])

    # выводим текст задания и меняем клавиатуру
    await message.reply('text', reply_markup=keyboard_quiz(**check_questions_len(lecture['questions'], 0)))  # TODO
    if lecture['questions'][0]['type'] == 'scalar':
        await message.answer('варианты ответов: ',
                             reply_markup=keyboard_answer_variants(lecture['questions'][0]['variants']))
        await state.set_state(Quiz.variants_question)
    elif lecture['questions'][0]['type'] == 'moderfile':
        await message.answer('напишите ответ самостоятельно')
        await state.set_state(Quiz.scalare_question)
    else:
        teacher = future_api.get_info_current_subject(message.from_user.id, state_data['subject_id'])['teacher']
        teacher_name = teacher['firstname'] + ' ' + teacher['lastname']
        await message.answer(f'отправьте файл с решением в виде PDF-файла. {teacher_name} проверит работу.')
        await state.set_state(Quiz.moderfile_question)
    state_data['lecture_quiz'] = lecture['questions']
    state_data['question_id'] = 0
    state_data['questions_answer'] = {}
    await state.set_data(state_data)


@lecture_router.message(Quiz.variants_question, F.text == "<")
@lecture_router.message(Quiz.scalare_question, F.text == "<")
@lecture_router.message(Quiz.moderfile_question, F.text == "<")
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data['question_id'] <= 0:
        return
    await message.reply('text', reply_markup=keyboard_quiz( # отправляем задание пользователю и справлем keyboard в случае необходимсти (1 задание или последнее)
        **check_questions_len(state_data['lecture_quiz']['questions'], state_data['question_id'])))  # TODO ['questions']
    # три типа вопросов: тест, точный ответ - ручной ввод, оправка решения в виде файла
    if state_data['lecture_quiz']['questions'][state_data['question_id'] - 1]['type'] == 'scalar':
        await message.answer('варианты ответов: ',
                             reply_markup=keyboard_answer_variants(
                                 state_data['lecture_quiz']['questions'][state_data['question_id'] - 1]['variants']))
        await state.set_state(Quiz.variants_question)
    elif state_data['lecture_quiz']['questions'][state_data['question_id'] - 1]['type'] == 'moderfile':
        await message.answer('напишите ответ самостоятельно')
        await state.set_state(Quiz.scalare_question)
    else:
        teacher = future_api.get_info_current_subject(message.from_user.id, state_data['subject_id'])['teacher']
        teacher_name = teacher['firstname'] + ' ' + teacher['lastname']
        await message.answer(f'отправьте файл с решением в виде PDF-файла. {teacher_name} проверит работу.')
        await state.set_state(Quiz.moderfile_question)
    # отнимаем единицу потому что ученик нажал на '<'
    state_data['question_id'] = state_data['question_id'] - 1
    await state.set_data(state_data)


@lecture_router.message(Quiz.variants_question, F.text == ">")
@lecture_router.message(Quiz.scalare_question, F.text == ">")
@lecture_router.message(Quiz.moderfile_question, F.text == ">")
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data['question_id'] >= len(state_data['lecture_quiz']):
        return
    if state_data['question_id'] == len(state_data['lecture_quiz']): # ученик дошел до конца теста
        await message.answer('Конец теста')
        answers = ''
        for i in range(len(state_data['lecture_quiz'])):
            try:
                answers += f'\n{i+1} задание - ' + state_data['questions_answer'][i] # отдаем ответы, созранившиеся в state_data['questions_answer']
            except KeyError: # если ученик не ответи на какойто вопрос, пропускаем этот вопрос
                pass

        await message.answer(f'Ваши ответы: {answers}')
    else:
        await message.reply('text', reply_markup=keyboard_quiz(
            **check_questions_len(state_data['lecture_quiz']['questions'], state_data['question_id']) # отправляем задание пользователю и справлем keyboard в случае необходимсти (1 задание или последнее)
        ))  # TODO ['questions']

        # три типа вопросов: тест, точный ответ - ручной ввод, оправка решения в виде файла
        if state_data['lecture_quiz']['questions'][state_data['question_id'] + 1]['type'] == 'scalar':
            await message.answer('варианты ответов: ',
                                 reply_markup=keyboard_answer_variants(
                                     state_data['lecture_quiz']['questions'][state_data['question_id'] + 1]['variants']))
            await state.set_state(Quiz.variants_question)
        elif state_data['lecture_quiz']['questions'][state_data['question_id'] + 1]['type'] == 'moderfile':
            await message.answer('напишите ответ самостоятельно')
            await state.set_state(Quiz.scalare_question)
        else:
            teacher = future_api.get_info_current_subject(message.from_user.id, state_data['subject_id'])['teacher']
            teacher_name = teacher['firstname'] + ' ' + teacher['lastname']
            await message.answer(f'отправьте файл с решением в виде PDF-файла. {teacher_name} проверит работу.')
            await state.set_state(Quiz.moderfile_question)
    # пррибавляем единицу потому что ученик нажал на '>'
    state_data['question_id'] = state_data['question_id'] + 1
    await state.set_data(state_data)


@lecture_router.message(Quiz.variants_question)
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lecture = future_api.get_lecture_by_number(state_data['subject_id'], state_data['lecture_id'])
    if message.text in lecture['questions'][state_data['question_id']]['variants']:
        # сохраняем ответ в state_data['questions_answer'][state_data['question_id']]
        state_data['questions_answer'][state_data['question_id']] = message.text
        await message.answer('Ответ принят')


@lecture_router.message(Quiz.scalare_question)
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    # сохраняем ответ в state_data['questions_answer'][state_data['question_id']]
    state_data['questions_answer'][state_data['question_id']] = message.text
    await message.answer('Ответ принят')


@lecture_router.message(Quiz.moderfile_question, F.document)
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    # сохраняем ответ в state_data['questions_answer'][state_data['question_id']]
    state_data['questions_answer'][state_data['question_id']] = message.document.file_id
    await message.answer('Ответ принят')
