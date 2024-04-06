from ..exceptions import ItemAlreadyExistsException, ItemException, ItemNotFoundException


class StudentException(ItemException):
    item = "student"

class StudentNotFoundException(StudentException, ItemNotFoundException):
    pass


class StudentAlreadyExistsException(StudentException, ItemAlreadyExistsException):
    pass
