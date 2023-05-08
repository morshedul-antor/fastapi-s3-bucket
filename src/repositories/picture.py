from schemas import PictureIn, PictureUpdate
from models import Picture
from repositories import BaseRepo


picture_repo = BaseRepo[Picture, PictureIn, PictureUpdate](Picture)

