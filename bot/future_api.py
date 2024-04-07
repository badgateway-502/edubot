from typing import Dict, List, TypedDict

import requests

from bot.entity_types import SubjectType, SubjectTitle_IdType, LectureType


# проверка существует ли пользователь
def check_user_db(user_id: int):
    headers = {'accept': 'application/json'}
    student = requests.get(f'http://127.0.0.1:8000/students/{user_id}', headers=headers)
    return True if student.status_code == 200 else False


def get_academic_performance(subject_id: int, user_id: int) -> float:
    return 2
    # TODO


# title=True => return lecture.title
# title=False => return lecture
def get_current_lecture_db(user_id: int, subject_id: int, tittle: bool = False) -> Dict[str, str] | str:
    pass
    # TODO


# получаем лекцию по ее номеру в предмете
def get_lecture_by_number(subject_id: int, lecture_number: int) -> LectureType:
    headers = {'accept': 'application/json'}
    lecture = requests.get(f'http://127.0.0.1:8000/subjects/{subject_id}/lectures/{lecture_number}', headers=headers)
    print(lecture.json())
    return lecture.json()


# получаем все доступные лекции в предмете
def get_lectures_all_db(subject_id: int) -> List[LectureType]:
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
    user = requests.get(f'http://127.0.0.1:8000/students/{user_id}', headers=headers)
    if user.status_code == 200:
        user = user.json()

        headers = {'accept': 'application/json'}
        performance = requests.get(f'http://127.0.0.1:8000/solutions/progress?student_id=840307055', headers=headers)
        performance = performance.json()
        bebra = {
            'Пройдено лабораторных работ': performance['labs_passed'],
            'Пройдено тестов': performance['tests_passed']
        }

        dicto = {
            'name': user['firstname'],
            'surname': user['lastname'],
            'academic_performance': bebra
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


def post_quiz_result(user_id, test_id, answers: Dict[int, str], questions) -> (int, int):

    weights = 0
    obsheee = 0
    print(answers)
    print(questions)
    for k, question in enumerate(questions):
        right_text = ''
        variki = question['variants']
        for varik in variki:
            if varik['is_right']:
                right_text = varik['text']
                break
        if k in answers.keys() and answers[k] == right_text:
            weights += question['weight']
        obsheee += question['weight']

    params = {
        "result": weights,
        "student_id": user_id,
        "test_id": test_id,
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    requests.post('http://127.0.0.1:8000/solutions/tests', json=params, headers=headers)

    return weights, obsheee


def post_lab(user_id, lab_id):
    headers = {'accept': 'application/json', 'Content-Type': 'multipart/form-data'}
    requests.post(f'http://127.0.0.1:8000/solutions/labs?student_id={user_id}&lab_id={lab_id}', headers=headers)

