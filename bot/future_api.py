async def check_user_db(user_id: int):
    if user_id == 840307055:
        return True
    else:
        return False


async def get_academic_performance_of_current_subject_db(subject: str, user_id: int):
    if user_id == 840307055:
        if subject == 'math':
            return 100
        if subject == 'english':
            return 100
        if subject == 'chemistry':
            return 100
        if subject == 'programming':
            return 100
        if subject == 'history':
            return 100


async def get_whole_score_of_current_subject_db(subject):
    if subject == 'math':
        return 120
    if subject == 'english':
        return 120
    if subject == 'chemistry':
        return 120
    if subject == 'programming':
        return 120
    if subject == 'history':
        return 120


async def get_available_subjects_db():
    dicto = ['math', 'english', 'chemistry', 'programming', 'history']
    return dicto


async def get_info_user_db(user_id: int):
    available_subjects = await get_available_subjects_db()
    academic_performance = {}
    for subject in available_subjects:
        academic_performance[subject]: float = round(
            await get_academic_performance_of_current_subject_db(subject, user_id) / (
                await get_whole_score_of_current_subject_db(subject)) * 100, 2)

    dicto = {
        'id': 840307055,
        'name': 'Кирилл',
        'surname': 'Подковырин',
        'academic_performance': academic_performance
    }
    return dicto


async def create_new_student(name: str, surname: str, user_id: int):
    assert name, str
    assert surname, str
    assert user_id, int
    # post
