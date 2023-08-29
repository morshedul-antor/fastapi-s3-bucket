from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from schemas import ImageOut, TodoIn
from services import image_service
from db import get_db, settings
from exceptions import handle_result
from sqlalchemy.orm import Session
from typing import Optional, List


router = APIRouter()


@router.get('/s3/', response_model=List[ImageOut])
def all_s3_bucket_images(db: Session = Depends(get_db)):
    data = image_service.get(db=db)
    return handle_result(data)


@router.post('/s3')
async def add_image_in_s3_bucket(file: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    data = await image_service.add_image_bucket(db=db, file=file)
    return data


@router.delete("/s3/delete")
async def delete_object(folder: str, file_name: str, db: Session = Depends(get_db)):
    delete = await image_service.delete_image_bucket(
        db=db, folder=folder, file_name=file_name)
    return delete


# ************** without service ************* #

# @router.post('/db', response_model=ImageOut)
# def add_image(logo: Optional[UploadFile] = File(None), banner: Optional[UploadFile] = File(None), image_data: TodoIn = Depends(),  db: Session = Depends(get_db)):
#     create = image_service.add_image(
#         db=db, logo=logo, banner=banner, data_in=image_data)
#     return handle_result(create)


# @router.get("/s3/{file_name}")
# async def view_image(file_name: str):
#     try:
#         key = f"static-assests/{file_name}"
#         url = f"https://s3.{settings.BUCKET_REGION}.amazonaws.com/{settings.BUCKET_NAME}/{key}"

#         return {"img_url": url}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal Server Error")
