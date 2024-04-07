from ..exceptions import ItemAccessDeniedException, ItemAlreadyExistsException, ItemException, ItemNotFoundException


class LabsSolution(ItemException):
    item = "labs solution"


class LabsSolutionNotFoundException(LabsSolution, ItemNotFoundException):
    pass


class LabsSolutionAlreadyExistsException(LabsSolution, ItemAlreadyExistsException):
    pass


class LabSolutionAccessDeniedException(LabsSolution, ItemAccessDeniedException):
    pass
