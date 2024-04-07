from ..exceptions import (
    ItemAlreadyExistsException,
    ItemException,
    ItemNotFoundException,
    ItemAccessDeniedException,
)


class TelegramException(Exception):
    pass


class SubjectException(ItemException):
    item = "subject"


class LectureLabException(ItemException):
    item = "lecture lab"


class LectureException(ItemException):
    item = "lecture"


class SubjectAlreadyExistsException(SubjectException, ItemAlreadyExistsException):
    pass


class SubjectNotFoundException(SubjectException, ItemNotFoundException):
    pass


class SubjectAccessException(SubjectException, ItemAccessDeniedException):
    pass


class LectureAlreadyExistsException(LectureException, ItemAlreadyExistsException):
    pass


class LectureNotFoundException(LectureException, ItemNotFoundException):
    pass


class LectureAccessException(LectureException, ItemAccessDeniedException):
    pass


class LectureLabNotFoundException(LectureLabException, ItemNotFoundException):
    pass


class LectureLabAlreadyExistsException(LectureLabException, ItemAlreadyExistsException):
    pass