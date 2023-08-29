from sqlalchemy import Column, String, Text, ForeignKey, Integer, Boolean
from models import BaseModel


class ToDo(BaseModel):
    __tablename__ = "todo"
    title = Column(String(255))
    task = Column(Text, nullable=True)


class Image(BaseModel):
    __tablename__ = "Images"
    service_name = Column(String(255), nullable=True)
    image_string = Column(String(255), nullable=True)
    bucket_string = Column(String(255), nullable=True)
    bucket_folder = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    bucket = Column(Boolean, nullable=True, default=False)
    todo_id = Column(Integer, ForeignKey("todo.id"))


class Picture(BaseModel):
    __tablename__ = "Pictures"
    service_name = Column(String(255), nullable=True)
    image_string = Column(String(255), nullable=True)
    todo_id = Column(Integer, ForeignKey("todo.id"))
