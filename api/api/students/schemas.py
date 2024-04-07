from pydantic import BaseModel


class StudentSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    firstname: str
    lastname: str
