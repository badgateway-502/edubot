from pydantic import BaseModel, EmailStr


class TeacherCreate(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str


class TeacherPrivate(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: str
    firstname: str
    lastname: str


class TeacherPublic(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    firstname: str
    lastname: str


class TeacherUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    firstname: str | None = None
    lastname: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
