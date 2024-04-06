class ItemException(Exception):
    item = "item"

    def __init__(self, message: str) -> None:
        self.message = message


def format_refs(refs: dict[str, str]) -> str:
    return ' '.join(f"{key}={value!r}" for key, value in refs.items())


class ItemNotFoundException(ItemException):
    def __init__(self, **refs: str):
        self.message = f"{self.item} with {format_refs(refs)} not found"
        self.refs = refs


class ItemAlreadyExistsException(ItemException):
    def __init__(self, **refs: str):
        self.message = f"{self.item} with {format_refs(refs)} already exists"
        self.refs = refs


class ItemAccessDeniedException(ItemException):
    def __init__(self, **refs) -> None:
        self.message = f"Access to {self.item} with {format_refs(refs)} denied"
