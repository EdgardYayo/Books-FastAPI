from pydantic import BaseModel, Field
from typing import Optional

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config: # This is used for set an example of successfull book schema
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Edgard Pazos',
                'description': 'New book',
                'rating': 5
            }
        }