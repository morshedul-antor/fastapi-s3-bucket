from schemas import ImageIn, ImageUpdate, TodoIn, PictureIn
from repositories import image_repo
from models import Image
from services import BaseService, CreateSchemaType, todo_service
from sqlalchemy.orm import Session
from utils import UploadFileUtils
from exceptions import ServiceResult, AppException, handle_result
from db import settings
from fastapi import HTTPException

import uuid
import boto3
from io import BytesIO


class ImageService  (BaseService[Image, ImageIn, ImageUpdate]):

    def add_image(self, logo: str, banner: str, db: Session, data_in: CreateSchemaType):

        todo_data = TodoIn(
            title=data_in.title,
            task=data_in.task
        )

        create_todo = todo_service.create_with_flush(
            db, data_in=todo_data)

        # image
        logo_img = UploadFileUtils(file=logo)

        # prefix is the short service name
        logo_name = logo_img.upload_image(
            prefix='logo', path='./assets/img/logo', accepted_extensions=['jpg', 'jpeg', 'png'])

        logo_data = ImageIn(
            todo_id=handle_result(create_todo).id,
            service_name='logo',
            image_string=logo_name
        )

        add_logo = image_service.create_with_flush(
            db, data_in=logo_data)

        # image
        banner_img = UploadFileUtils(file=banner)

        # prefix is the short service name
        banner_name = banner_img.upload_image(
            prefix='banner', path='./assets/img/banner', accepted_extensions=['jpg', 'jpeg', 'png'])

        banner_data = PictureIn(
            todo_id=handle_result(create_todo).id,
            service_name='banner',
            image_string=banner_name
        )

        add_banner = image_service.create(
            db, data_in=banner_data)

        if not add_banner:
            return ServiceResult(AppException.ServerError(
                "Problem with image upload!"))
        else:
            return add_banner

# **************** S3 Bucket ****************** #
    async def add_image_bucket(db: Session, file: str):
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


image_service = ImageService(Image, image_repo)
