from ..exceptions import ItemAlreadyExistsException, ItemNotFoundException


class SubjectAlreadyExistsException(ItemAlreadyExistsException):
    item = "subject"


class SubjectNotFoundException(ItemNotFoundException):
    item = "subject"


class SubjectAccessException(Exception):
    def __init__(self, message: str = "Access denied") -> None:
        self.message = message
