from sqlalchemy import Column, Integer, String, Text
from db import Base

# Define To Do class inheriting from Base
class ToDo(Base):
       __tablename__ = 'todo'
       id = Column(Integer, primary_key=True)
       title = Column(String(255))
       task = Column(Text, nullable=True)