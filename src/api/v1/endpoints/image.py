from fastapi import APIRouter, Depends, UploadFile, File
from schemas import ImageOut, TodoIn
from services import image_service
from db import get_db
from exceptions import handle_result
from sqlalchemy.orm import Session
from typing import Optional


router = APIRouter()


@router.post('/', response_model=ImageOut)
def add_image(file: Optional[UploadFile] = File(None), image_data: TodoIn = Depends(),  db: Session = Depends(get_db)):
    create  = image_service.add_image(db=db, file=file, data_in=image_data)
    return handle_result(create)