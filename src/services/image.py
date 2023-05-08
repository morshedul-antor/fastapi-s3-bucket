from schemas import ImageIn, ImageUpdate, TodoIn, PictureIn
from repositories import image_repo
from models import Image
from services import BaseService, CreateSchemaType, todo_service
from sqlalchemy.orm import Session
from utils import UploadFileUtils
from exceptions import ServiceResult, AppException, handle_result


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


image_service = ImageService(Image, image_repo)