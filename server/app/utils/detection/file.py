import os
from typing import Union

from app.constants import DetectionItemType
from app.schemas.detection import DetectionItemCreate
from app.services import FileStorageService


AVAILABLE_IMAGE_EXTENSIONS = set([
    ".jpg",
    ".jpeg",
    ".png",
])
AVAILABLE_VIDEO_EXTENSIONS = set([
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
])


async def get_file_type(file_extension: str) -> bool:
    file_extension = file_extension.lower()
    if file_extension in AVAILABLE_VIDEO_EXTENSIONS:
        return DetectionItemType.VIDEO

    if file_extension in AVAILABLE_IMAGE_EXTENSIONS:
        return DetectionItemType.IMAGE
    
    return None


async def check_files_extension(files: list) -> Union[list[tuple[str, str]], str]:
    files_and_types = []
    uploaded_files = set()
    message = ""
    for file in files:
        if file in uploaded_files:
            continue
        file_type = ""
        _, file_extension = os.path.splitext(file.filename)
        
        file_type = await get_file_type(file_extension)

        if not file_type:
            message = f"Файлы с расширением {file_extension} не поддерживаются для совершения предсказания"
            return files_and_types, message

        uploaded_files.add(file)
        files_and_types.append((file, file_type))
    return files_and_types, message


async def create_items(
    file_service: FileStorageService,
    session,
    detection_item_repository,
    detection_task_uuid,
    upload_files,
) -> None:
    for file, type in upload_files:
        path = await file_service.save(detection_task_uuid, file)
        schema = DetectionItemCreate(
            origin_file=str(path),
            type=type,
            detection_id=detection_task_uuid,
        )
        await detection_item_repository.create(session, obj_in=schema)
