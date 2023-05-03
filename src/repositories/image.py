from schemas import ImageIn, ImageUpdate
from models import Image
from repositories import BaseRepo


image_repo = BaseRepo[Image, ImageIn, ImageUpdate](Image)

