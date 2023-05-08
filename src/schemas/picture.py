from pydantic import BaseModel
from typing import Optional


class PictureBase(BaseModel):
    service_name: Optional[str] = None
    image_string: Optional[str] = None


class PictureIn(PictureBase):
    todo_id: int


class PictureOut(PictureIn):
    id: int

    class Config:
        orm_mode = True


class PictureUpdate(PictureBase):
    pass


class PictureWithTodoIn(PictureBase):
    title: Optional[str] = None
    task: Optional[str] = None
