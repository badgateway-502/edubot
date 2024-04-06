from ..exceptions import ItemAlreadyExistsException, ItemNotFoundException


class StudentNotFoundException(ItemNotFoundException):
    item = "student"


class StudentAlreadyExistsException(ItemAlreadyExistsException):
    item = "student"
