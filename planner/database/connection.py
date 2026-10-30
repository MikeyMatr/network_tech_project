from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from models.events import Event
from models.users import UserAccount


database_file = Path(__file__).resolve().parent.parent / "planner.db"

engine = create_engine(
    f"sqlite:///{database_file}",
    echo=True,
    connect_args={"check_same_thread": False},
)


def conn():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session