from pydantic import BaseModel, ConfigDict, EmailStr, Field
from models.events import Event
from sqlmodel import SQLModel, Field as SQLField


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


class UserAccount(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    email: str = SQLField(unique=True, index=True)
    password_hash: str