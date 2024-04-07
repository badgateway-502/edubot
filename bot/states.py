from aiogram.fsm.state import StatesGroup, State


class AFKState(StatesGroup):
    logged = State()  # учник вошел в систему


class SignInState(StatesGroup):
    signing_in = State()  # ученик должен зарегестрироваться


class SubjectState(StatesGroup):
    choosing_subject = State()  # ученик выбирает предмет
    chosen_subject = State()  # ученик выбрал предмет
    choosing_lecture = State()  # ученик выбирает лекцию
    lecture_opened = State()  # ученик выбрал лецию в том числе текущую
    quiz_opened = State()  # ученик открыл тест


class Quiz(StatesGroup):
    variants_question = State()  # вопрос с вариантом ответов
    scalare_question = State()  # вопрос с без вариантов ответов
    moderfile_question = State()  # вопрос с пост модерацией
