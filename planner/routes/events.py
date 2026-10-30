from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models.users import UserAccount
from database.connection import get_session
from models.events import Event, EventCreate, EventUpdate


event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model=list[Event])
def retrieve_all_events(
    session: Session = Depends(get_session),
):
    return session.exec(
        select(Event).order_by(Event.id)
    ).all()


@event_router.get("/{id}", response_model=Event)
def retrieve_event(
    id: int,
    session: Session = Depends(get_session),
):
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return event


@event_router.post(
    "/new",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    body: EventCreate,
    session: Session = Depends(get_session),
):
    user = session.get(UserAccount, body.user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    event = Event.model_validate(body)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@event_router.put("/{id}", response_model=Event)
def update_event(
    id: int,
    body: EventUpdate,
    session: Session = Depends(get_session),
):
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    changes = body.model_dump(exclude_unset=True)

    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null",
        )

    for field, value in changes.items():
        setattr(event, field, value)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@event_router.delete("/{id}")
def delete_event(
    id: int,
    session: Session = Depends(get_session),
):
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    session.delete(event)
    session.commit()

    return {"message": "Event deleted successfully"}


@event_router.delete("/")
def delete_all_events(
    session: Session = Depends(get_session),
):
    for event in session.exec(select(Event)).all():
        session.delete(event)

    session.commit()

    return {"message": "Events deleted successfully"}

