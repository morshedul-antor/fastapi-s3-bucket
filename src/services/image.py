from schemas import ImageIn, ImageUpdate, TodoIn
from repositories import image_repo
from models import Image
from services import BaseService, CreateSchemaType, todo_service
from sqlalchemy.orm import Session
from utils import UploadFileUtils
from exceptions import ServiceResult, AppException, handle_result


class ImageService  (BaseService[Image, ImageIn, ImageUpdate]):
   
    def add_image(self, file: str, db: Session, data_in: CreateSchemaType):

        up_img = UploadFileUtils(file=file)

        # prefix is the short service name
        image_name = up_img.upload_image(
            prefix='logo', path='./assets/img/profile', accepted_extensions=['jpg', 'jpeg', 'png'])
        

        todo_data = TodoIn(
            title=data_in.title,
            task=data_in.task
        )

        create_todo = todo_service.create_with_flush(
            db, data_in=todo_data)


        image_data = ImageIn(
            todo_id=handle_result(create_todo).id,
            service_name='logo', 
            image_string=image_name
        )

        add_image = image_service.create(
            db, data_in=image_data)


        if not add_image:
            return ServiceResult(AppException.ServerError(
                "Problem with image upload!"))
        else:
            return add_image


image_service = ImageService(Image, image_repo)