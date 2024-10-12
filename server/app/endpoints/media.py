import io
import pathlib
import os

from fastapi import (
    APIRouter,
    Path,
    Request,
    responses,
    status,
)
from PIL import Image

from app.config import get_settings
from app.constants import DetectionItemType
from app.utils.detection import get_file_type


api_router = APIRouter(
    prefix="/media",
    tags=["Media"],
)


@api_router.get(
    "/{folder}/{filename}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Задача детекции не найдена",
        },
    },
)
async def get_detection_task(
    _: Request,
    folder: str = Path(...),
    filename: str = Path(...),
):
    settings = get_settings()

    path = pathlib.Path(settings.MEDIA_PATH) / folder / filename
    file_name, file_extension = os.path.splitext(filename)

    file_type = await get_file_type(file_extension)

    if file_type == DetectionItemType.IMAGE:
        image = Image.open(path)
        image_io = io.BytesIO()
        image.save(image_io, 'JPEG')
        image_io.seek(0)
        return responses.StreamingResponse(
            content=image_io,
            media_type="image/jpeg",
        )

    if file_type == DetectionItemType.VIDEO:
        if filename.startswith("predict"):
            path = pathlib.Path(settings.MEDIA_PATH) / folder / f"{file_name}.webm"
        with open(path, "rb") as video:
            data = video.read()
            return responses.Response(data, media_type="video/webm")
