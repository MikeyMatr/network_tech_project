from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event

event_router = APIRouter(tags=["Events"])
events = []


@event_router.get("/", response_model=list[Event])
async def retrieve_all_events() -> list[Event]:
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    for event in events:
        if event.id == body.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event with supplied ID already exists"
            )
    events.append(body)
    return {"message": "Event created successfully"}


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "Events deleted successfully"}


@event_router.put('/{id}')
async def update_event(id: int, body: Event = Body(...)) -> dict:
    for index, event in enumerate(events):
        if event.id == id:
            if body.id != id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Event ID cannot be changed"
                )
            events[index] = body
            return {"message": "Event updated successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )