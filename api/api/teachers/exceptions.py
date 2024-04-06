from ..exceptions import ItemAlreadyExistsException, ItemNotFoundException


class TeacherNotFoundException(ItemNotFoundException):
    item = "teacher"


class AuthenticationException(Exception):
    def __init__(self, message: str = "wrong email or password"):
        self.message = message


class TeacherAlreadyExistsException(ItemAlreadyExistsException):
    item = "teacher"
