from aiogram.fsm.state import StatesGroup, State


class AFKState(StatesGroup):
    logged = State()  # учник вошел в систему


class SignInState(StatesGroup):
    signing_in = State()  # ученик должен зарегестрироваться


class SubjectState(StatesGroup):
    choosing_subject = State()  # ученик выбирает предмет
    chosen_subject = State()  # ученик выбрал предмет
    choosing_lecture = State()  # ученик выбирает лекцию
    lecture_opened = State()  # ученик выбрал лецию старую
    lecture_current_opened = State()  # ученик выбрал текущую лецию
    quiz_opened = State()  # ученик открыл тест


class Lab(StatesGroup):
    lab_opened = State()  # ученик хочет сдать лаб работу


class Quiz(StatesGroup):
    variants_question = State()  # вопрос с вариантом ответов
    scalare_question = State()  # вопрос с без вариантов ответов
    finish_quiz = State()  # учениr на стоит перде выбором закончить ли тест?
    finished_quiz = State()  # учениr получил результат теста
