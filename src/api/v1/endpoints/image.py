from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from schemas import ImageOut, TodoIn
from services import image_service
from db import get_db, settings
from exceptions import handle_result
from sqlalchemy.orm import Session
from typing import Optional

import uuid
import boto3
from io import BytesIO


router = APIRouter()


@router.post('/db', response_model=ImageOut)
def add_image(logo: Optional[UploadFile] = File(None), banner: Optional[UploadFile] = File(None), image_data: TodoIn = Depends(),  db: Session = Depends(get_db)):
    create = image_service.add_image(
        db=db, logo=logo, banner=banner, data_in=image_data)
    return handle_result(create)


@router.post('/s3')
async def add_image_bucket(file: UploadFile = File(...), db: Session = Depends(get_db)):
    identifier = str(uuid.uuid4())

    file_name = f"{identifier}_{file.filename}"
    folder = f"static-assests/{file_name}"

    s3_client = boto3.client(
        's3', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)

    try:
        content = await file.read()
        s3_client.put_object(
            Bucket=settings.BUCKET_NAME,
            Key=folder,
            Body=BytesIO(content)
        )
        url = f"https://s3.{settings.BUCKET_REGION}.amazonaws.com/{settings.BUCKET_NAME}/{folder}"

        return {"status": "success", 'img_url': url}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error")


@router.get("/s3/{file_name}")
async def view_image(file_name: str):
    try:
        key = f"static-assests/{file_name}"
        url = f"https://s3.{settings.BUCKET_REGION}.amazonaws.com/{settings.BUCKET_NAME}/{key}"

        return {"img_url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/s3/delete/{object_key}")
async def delete_object(folder: str, file_name: str):
    s3_client = boto3.client(
        's3', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)

    try:
        object_key = f"{folder}/{file_name}"

        s3_client.delete_object(
            Bucket=settings.BUCKET_NAME,
            Key=object_key
        )

        return {"status": "success", "message": f"Object '{object_key}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
