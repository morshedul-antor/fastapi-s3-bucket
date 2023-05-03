from fastapi import APIRouter, Depends, UploadFile, File, Form
from schemas import ImageOut, TodoIn
from services import image_service
from db import get_db
from exceptions import handle_result
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/', response_model=ImageOut)
def add_image(file: UploadFile = File(...), image_data: TodoIn = Depends(),  db: Session = Depends(get_db)):
    create  = image_service.add_image(db=db, file=file, data_in=image_data)
    return handle_result(create)
