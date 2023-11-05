from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=200)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)
