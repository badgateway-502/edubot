from typing import List, Dict

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot import future_api
from bot.keyboards import keyboard_quiz, keyboard_answer_variants, keyboard_to_current_lecture, lab_opened
from bot.states import SubjectState, Lab
from bot.states import Quiz

lecture_router = Router()


# функция для проверки того на каком вопросе находится ученик и нужно ли менять калвиатуру
def check_questions_len(questions: List, question_id_now: int) -> Dict[str, bool]:
    if question_id_now <= 0:
        return {'first': True}
    elif question_id_now >= len(questions):
        return {'last': True}
    return {}


@lecture_router.message(SubjectState.lecture_opened, F.text == "Сдать лаб работу")
async def post_lab_work(message: types.Message, state: FSMContext):
    lab_work = future_api.get_lecture_by_number((await state.get_data())['subject_id'], (await state.get_data())['lecture_id'])['lab']

    await message.reply(lab_work['text_description'] + '\n\n отправьте лабораторную работу файлом', reply_markup=lab_opened())
    await state.set_state(Lab.lab_opened)


@lecture_router.message(Lab.lab_opened, F.document)
async def post_lab_work(message: types.Message):
    future_api.post_lab(message.from_user.id, message.document.file_id)
    await message.reply('Лабораторная работа отправленна', reply_markup=keyboard_to_current_lecture())



@lecture_router.message(SubjectState.lecture_opened, F.text == "Пройти тест")
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lecture = future_api.get_lecture_by_number(state_data['subject_id'], state_data['lecture_id'])
    state_data['lecture_quiz'] = lecture['test']['questions']
    state_data['question_id'] = 0
    state_data['test_id'] = lecture['test']['id']
    state_data['questions_answer'] = {}

    questions = state_data['lecture_quiz']
    quest_id = state_data['question_id']

    # выводим текст задания и меняем клавиатуру
    await message.reply(questions[quest_id]["question"], reply_markup=keyboard_quiz(**check_questions_len(questions, 0)))
    if questions[0]['type'] == 'variant':
        await message.answer('варианты ответов: ', reply_markup=keyboard_answer_variants(questions[0]['variants']))
        await state.set_state(Quiz.variants_question)
    elif questions[0]['type'] == 'scalar':
        await message.answer('напишите ответ самостоятельно')
        await state.set_state(Quiz.scalare_question)
    await state.set_data(state_data)


@lecture_router.message(Quiz.variants_question, F.text == "<")
@lecture_router.message(Quiz.scalare_question, F.text == "<")
@lecture_router.message(Quiz.finish_quiz, F.text == "<")
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    questions = state_data['lecture_quiz']
    quest_id = state_data['question_id'] - 1
    answers = state_data['questions_answer']

    if quest_id < 0:
        return
    if quest_id in answers.keys():
        user_answer = answers[quest_id]
        # если ученик уже ответи на этот вопрос сообщаем ему об этом
        await message.reply(questions[quest_id]["question"] + f'\n\nВаш ответ {user_answer}',
                            reply_markup=keyboard_quiz(**check_questions_len(questions, quest_id)))
        # TODO ['questions']
    else:
        # отправляем задание пользователю и справлем keyboard в случае необходимсти (1 задание или последнее)
        await message.reply(questions[quest_id]["question"],
                            reply_markup=keyboard_quiz(**check_questions_len(questions, quest_id)))
    # три типа вопросов: тест, точный ответ - ручной ввод, оправка решения в виде файла
    if questions[quest_id]['type'] == 'variant':
        await message.answer('варианты ответов: ',
                             reply_markup=keyboard_answer_variants(questions[quest_id]['variants']))
        await state.set_state(Quiz.variants_question)
    elif questions[quest_id]['type'] == 'scalar':
        await message.answer('напишите ответ самостоятельно')
        await state.set_state(Quiz.scalare_question)
    # отнимаем единицу потому что ученик нажал на '<'
    state_data['question_id'] = quest_id
    await state.set_data(state_data)


@lecture_router.message(Quiz.variants_question, F.text == ">")
@lecture_router.message(Quiz.scalare_question, F.text == ">")
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    questions = state_data['lecture_quiz']
    quest_id = state_data['question_id'] + 1
    answers = state_data['questions_answer']
    if quest_id > len(questions):
        return
    if quest_id >= len(questions):  # ученик дошел до конца теста
        await message.answer('Конец теста')
        answers_finish = ''
        for i in range(len(questions)):
            try:
                answers_finish += f'\n{i + 1} задание - ' + answers[i]
                # отдаем ответы, сохранившиеся в state_data['questions_answer']
            except KeyError:  # если ученик не ответи на какойто вопрос, пропускаем этот вопрос
                pass
        print(quest_id)
        await message.answer(f'Ваши ответы: {answers_finish}',
                             reply_markup=keyboard_quiz(**check_questions_len(questions, quest_id)))
        await state.set_state(Quiz.finish_quiz)
    else:
        if quest_id in answers.keys():
            user_answer = answers[quest_id]
            # если ученик уже ответи на этот вопрос сообщаем ему об этом
            await message.reply(questions[quest_id]["question"] + f'\n\nВаш ответ {user_answer}',
                                reply_markup=keyboard_quiz(**check_questions_len(questions, quest_id)))
            # TODO ['questions']
        else:
            # отправляем задание пользователю и справлем keyboard в случае необходимсти (1 задание или последнее)
            await message.reply(questions[quest_id]["question"],
                                reply_markup=keyboard_quiz(**check_questions_len(questions, quest_id)))

        # три типа вопросов: тест, точный ответ - ручной ввод, оправка решения в виде файла
        if questions[quest_id]['type'] == 'variant':
            await message.answer('варианты ответов: ',
                                 reply_markup=keyboard_answer_variants(
                                     questions[quest_id]['variants']))
            await state.set_state(Quiz.variants_question)
        elif questions[quest_id]['type'] == 'scalar':
            await message.answer('напишите ответ самостоятельно')
            await state.set_state(Quiz.scalare_question)
    # пррибавляем единицу потому что ученик нажал на '>'
    state_data['question_id'] = quest_id
    await state.set_data(state_data)


@lecture_router.callback_query(Quiz.variants_question)
async def my_subjects_button(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    questions = state_data['lecture_quiz']
    quest_id = state_data['question_id']
    varik = []
    print(123)
    for i in questions[quest_id]['variants']:
        varik.append(i['text'])
    print(varik)
    print(callback.data)
    if callback.data in varik:
        # сохраняем ответ в state_data['questions_answer'][state_data['question_id']]
        state_data['questions_answer'][state_data['question_id']] = callback.data
        await callback.message.answer('Ответ принят')


@lecture_router.message(Quiz.scalare_question)
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    # сохраняем ответ в state_data['questions_answer'][state_data['question_id']]
    state_data['questions_answer'][state_data['question_id']] = message.text
    await message.answer('Ответ принят')


@lecture_router.message(Quiz.finish_quiz, F.text == 'Закончить тест')
async def my_subjects_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    results = future_api.post_quiz_result(message.from_user.id, state_data['test_id'], state_data['questions_answer'], state_data['lecture_quiz'])
    await message.answer(f'Ваши результаты:\n{results[0]} из {results[1]}', reply_markup=keyboard_to_current_lecture())
    await state.set_state(Quiz.finished_quiz)
