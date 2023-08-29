from services import BaseService, CreateSchemaType, todo_service
from schemas import ImageIn, ImageUpdate, TodoIn, PictureIn
from exceptions import ServiceResult, AppException, handle_result
from fastapi import HTTPException, UploadFile
from repositories import image_repo
from sqlalchemy.orm import Session
from utils import UploadFileUtils
from models import Image
from db import settings

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
    async def add_image_bucket(self, db: Session, file: UploadFile):
        object_key = 'static-assests/ed237519-86e6-4de6-8c00-29bea5d291dc_logo.png'

        if file:
            identifier = str(uuid.uuid4())
            file_name = f"{identifier}_{file.filename}"
            folder = f"logo/{file_name}"

            s3_client = boto3.client(
                's3', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)

            try:
                # delete previous image
                s3_client.delete_object(
                    Bucket=settings.BUCKET_NAME,
                    Key=object_key
                )

                content = await file.read()
                s3_client.put_object(
                    Bucket=settings.BUCKET_NAME,
                    Key=folder,
                    Body=BytesIO(content)
                )

                url = f"https://s3.{settings.BUCKET_REGION}.amazonaws.com/{settings.BUCKET_NAME}/{folder}"

                logo_data = ImageIn(
                    todo_id=1,
                    service_name='logo',
                    bucket_string=file_name,
                    bucket_folder='logo',
                    image_url=url,
                    bucket=True,
                )

                add_logo = image_service.create(
                    db, data_in=logo_data)

                if add_logo:
                    return {"status": "success", "img_url": url, "img_delete": object_key}

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail="Internal Server Error")
        else:
            logo_data = ImageIn(
                todo_id=1,
                service_name='logo',
                bucket=False,
            )

            add_logo = image_service.create(
                db, data_in=logo_data)

            if add_logo:
                return {"status": "success", "message": 'DB in without image!'}

    async def delete_image_bucket(self, db: Session, folder: str, file_name: str):
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
            raise HTTPException(
                status_code=500, detail="Internal Server Error")


image_service = ImageService(Image, image_repo)
