from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: list[str]
    location: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "title": "FastAPI Book Launch",
            "image": "https://example.com/image.png",
            "description": "Discussion of the FastAPI book.",
            "tags": ["python", "fastapi", "book"],
            "location": "Google Meet"
        }
    })
