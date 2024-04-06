class TeacherNotFoundException(Exception):
    def __init__(self, **refs: str):
        self.message = f"teacher with {' '.join(f"{key}={value}" for key, value in refs.items())} not found"
        self.refs = refs


class AuthenticationException(Exception):
    def __init__(self, message: str = "wrong email or password"):
        self.message = message


class TeacherAlreadyExistsException(Exception):
    def __init__(self, **refs: str):
        self.message = f"teacher with {' '.join(f"{key}={value}" for key, value in refs.items())} already exists"
