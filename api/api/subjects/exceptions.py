from ..exceptions import (
    ItemAlreadyExistsException,
    ItemException,
    ItemNotFoundException,
    ItemAccessDeniedException,
)


class SubjectException(ItemException):
    item = "subject"


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
