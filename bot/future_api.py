from config_reader import config

async def check_user_db(user_id: int):
    if user_id == int(config.your_tg_id.get_secret_value()):
        return True
    else:
        return False


async def get_academic_performance_of_current_subject_db(subject: int, user_id: int):
    if user_id == int(config.your_tg_id.get_secret_value()):
        if subject == 0:
            return 100
        if subject == 1:
            return 100
        if subject == 2:
            return 100


async def get_whole_score_of_current_subject_db(subject: int):
    if subject == 0:
        return 120
    if subject == 1:
        return 120
    if subject == 2:
        return 120


async def get_academic_performance(subject_id: int, user_id: int) -> float:
    academic_performance: float = round(
        await get_academic_performance_of_current_subject_db(subject_id, user_id) / (
            await get_whole_score_of_current_subject_db(subject_id)) * 100, 2)
    return academic_performance


async def get_info_about_subject_db(user_id: int, subject_id=None) -> tuple[int, str, str, float] | \
                                                                      list[tuple[int, str, str, float]]:
    dicto = [(1, 'math', 'mihail voronov', await get_academic_performance(0, user_id)),
             (2, 'english', 'gleb mishustin', await get_academic_performance(1, user_id)),
             (3, 'programming', 'dmitriy popov', await get_academic_performance(2, user_id)),
             ]
    if subject_id or subject_id == 0:
        for i in dicto:
            if i[0] == subject_id:
                return i
        raise ValueError('Такого предмета нет')
    return dicto


async def get_info_user_db(user_id: int):
    available_subjects = await get_info_about_subject_db(user_id)
    academic_performance = {}
    for subject in available_subjects:
        academic_performance[subject[1]]: float = subject[3]

    dicto = {
        'id': int(config.your_tg_id.get_secret_value()),
        'name': 'Кирилл',
        'surname': 'Подковырин',
        'academic_performance': academic_performance
    }
    return dicto


async def create_new_student_db(name: str, surname: str, user_id: int):
    assert name, str
    assert surname, str
    assert user_id, int
    # post


async def get_info_about_subject(user_id: int, subject_id: int) -> tuple[int, str, str, float]:
    info: tuple[int, str, str, float] = await get_info_about_subject_db(user_id, subject_id)
    return info
