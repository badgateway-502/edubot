from ..exceptions import ItemException, ItemNotFoundException, ItemAlreadyExistsException


class AuthenticationException(Exception):
    def __init__(self, message: str = "wrong email or password"):
        self.message = message


class TeacherException(ItemException):
    item = "tacher"

class TeacherNotFoundException(TeacherException, ItemNotFoundException):
    pass


class TeacherAlreadyExistsException(TeacherException, ItemAlreadyExistsException):
    pass
