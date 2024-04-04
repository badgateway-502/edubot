import re
import string
# import pydantic


def validate_name(name: str):
    if len(name) > 40:
        raise ValueError("Длина вашего имени не может быть больше сорока символов")
    elif bool(re.search(r'\d', name)):
        raise ValueError("Ваше имя не должно содержать цифры")
    elif any(character in string.punctuation for character in name):
        raise ValueError(f"Ваше имя не должно содержать следующие символы: {string.punctuation}")
    elif len(name.split()) != 2:
        raise ValueError("Пожалуйста, напишите Ваше имя и фамилию через пробел")
    return True
