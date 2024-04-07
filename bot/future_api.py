from typing import Dict, List, TypedDict

import requests

from bot.entity_types import SubjectType, SubjectTitle_IdType, LectureType
from config_reader import config
from lectures import *

# проверка существует ли пользователь
def check_user_db(user_id: int):
    headers = {'accept': 'application/json'}
    student = requests.get(f'http://127.0.0.1:8000/students{user_id}', headers=headers)
    return True if student.status_code == 200 else False


def get_academic_performance_of_current_subject_db(subject: int, user_id: int):
    if user_id == int(config.your_tg_id.get_secret_value()):
        if subject == 1:
            return 100
        if subject == 2:
            return 100
        if subject == 3:
            return 100


def get_whole_score_of_current_subject_db(subject: int):
    if subject == 1:
        return 120
    if subject == 2:
        return 120
    if subject == 3:
        return 120


def get_academic_performance(subject_id: int, user_id: int) -> float:
    academic_performance: float = round(
        get_academic_performance_of_current_subject_db(subject_id, user_id) / (
            get_whole_score_of_current_subject_db(subject_id)) * 100, 2)
    return academic_performance


# title=True => return lecture.title
# title=False => return lecture
def get_current_lecture_db(user_id: int, subject_id: int, tittle: bool = False) -> Dict[str, str] | str:
    if user_id == int(config.your_tg_id.get_secret_value()):
        if subject_id == 1:
            if tittle:
                return math_lectures[0]['title']
            return math_lectures[0]
        if subject_id == 2:
            if tittle:
                return english_lectures[0]['title']
            return english_lectures[0]
        if subject_id == 3:
            if tittle:
                return program_lecture[0]['title']
            return program_lecture[0]
    # TODO

# получаем лекцию по ее номеру в предмете
def get_lecture_by_number(subject_id: int, lecture_number: int) -> LectureType:
    headers = {'accept': 'application/json'}
    lecture = requests.get(f'http://127.0.0.1:8000/subjects/{subject_id}/lectures/{lecture_number}', headers=headers)
    return lecture.json()


# получаем все доступные лекции в предмете
def get_lectures_all_db(user_id: int, subject_id: int) -> List[LectureType]:
    headers = {'accept': 'application/json'}
    subject = requests.get(f'http://127.0.0.1:8000/subjects/{subject_id}', headers=headers)
    return subject.json()['lectures']

# получаем информацию о предмете - название, преподавателя, который ведет предмет, успеваемость ученика по предмету
def get_info_current_subject(user_id: int, subject_id: int) -> SubjectType:
    headers = {'accept': 'application/json'}
    subject = requests.get(f'http://127.0.0.1:8000/subjects/{subject_id}', headers=headers)
    # TODO academic performance

    return subject.json()

# получить все предметы
def get_info_about_subjects_db() -> List[SubjectType]:
    headers = {'accept': 'application/json'}
    subjects = requests.get('http://127.0.0.1:8000/subjects/', headers=headers)

    # TODO academic performance

    return subjects.json()

# получить все названия предметов и из идентификатор
def get_subjects_titles() -> SubjectTitle_IdType:
    headers = {'accept': 'application/json'}
    subjects = requests.get('http://127.0.0.1:8000/subjects/', headers=headers)
    titles = {subject['name']: subject['id'] for subject in subjects.json()}
    return titles

# получить информацию о пользователе - ФИ, успеваемость, текущие лекции.
def get_info_user_db(user_id: int):
    headers = {'accept': 'application/json'}
    user = requests.get(f'http://127.0.0.1:8000/students{user_id}', headers=headers)
    if user.status_code == 200:
        user = user.json()
        available_subjects = get_info_about_subjects_db(user_id)
        academic_performance = {}
        # for subject in available_subjects:
        #     academic_performance[subject[1]]: float = subject[3]

        dicto = { # TODO
            'name': user['firstname'],
            'surname': user['lastname'],
            'academic_performance': academic_performance
        }
        return dicto
    else:
        return False

# регистрация нового ученика, в начале, при вводе /start
def create_new_student_db(name: str, surname: str, user_id: int):
    params = {
        "id": user_id,
        "firstname": f"{name}",
        "lastname": f"{surname}",
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    requests.post('http://127.0.0.1:8000/students/', json=params, headers=headers)
