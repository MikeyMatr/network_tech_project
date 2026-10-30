from pydantic import ConfigDict
from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


class EventCreate(SQLModel):
    title: str
    image: str
    description: str
    tags: list[str]
    location: str

    model_config = ConfigDict(extra="forbid")


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: list[str] = Field(sa_column=Column(JSON, nullable=False))
    location: str


class EventUpdate(SQLModel):
    title: str | None = None
    image: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    location: str | None = None

    model_config = ConfigDict(extra="forbid")