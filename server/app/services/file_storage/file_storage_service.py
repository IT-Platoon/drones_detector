from pathlib import Path

from fastapi import UploadFile

from app.config import get_settings
from app.services.metaclasses import Singleton


class FileStorageService(metaclass=Singleton):
    CHUNK_SIZE = 4096
    HEXDIGITS = "0123456789abcdef"
    PATH = Path(get_settings().MEDIA_PATH)
    INITIALIZED = False

    def __init__(self):
        self.PATH.mkdir(exist_ok=True, parents=True)

    async def save(self, identifier: str, descriptor: UploadFile):
        directory = self.PATH / identifier
        directory.mkdir(exist_ok=True, parents=True)
        filepath = directory / descriptor.filename
        with open(filepath, "wb") as local_file:
            while buffer := await descriptor.read(self.CHUNK_SIZE):
                local_file.write(buffer)
        return filepath

    def delete(self, identifier: str, filename: str):
        (self.PATH / identifier / filename).unlink(missing_ok=True)

    def get_descriptor(self, path: str):
        return open(path, "rb")
