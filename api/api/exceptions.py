class ItemNotFoundException(Exception):
    item = "item"

    def __init__(self, **refs: str):
        self.message = f"{self.item} with {' '.join(f"{key}={value}" for key, value in refs.items())} not found"
        self.refs = refs


class ItemAlreadyExistsException(Exception):
    item = "item"

    def __init__(self, **refs: str):
        self.message = f"{self.item} with {' '.join(f"{key}={value}" for key, value in refs.items())} already exists"
        self.refs = refs
