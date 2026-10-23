from pydantic import BaseModel, ConfigDict, EmailStr, Field
from models.events import Event


class User(BaseModel):
    email: EmailStr
    events: list[Event] = Field(default_factory=list)


class NewUser(User):
    password: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "fastapi@packt.com",
            "password": "strong!!!",
            "events": []
        }
    })


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "fastapi@packt.com",
            "password": "strong!!!"
        }
    })
