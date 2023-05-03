from pydantic import BaseModel
from typing import Optional


class ImageBase(BaseModel):
    service_name: Optional[str] = None
    image_string: Optional[str] = None


class ImageIn(ImageBase):
    todo_id: int


class ImageOut(ImageIn):
    id: int

    class Config:
        orm_mode = True


class ImageUpdate(ImageBase):
    pass


class ImageWithTodoIn(ImageBase):
    title: Optional[str] = None
    task: Optional[str] = None
