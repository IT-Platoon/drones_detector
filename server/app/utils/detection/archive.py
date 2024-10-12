import io
import os
import zipfile

from app.db.models import DetectionTask


async def archive_detection_task(task: DetectionTask) -> io.BytesIO:
    zip_bytes_io = io.BytesIO()
    with zipfile.ZipFile(zip_bytes_io, 'w', zipfile.ZIP_DEFLATED) as zipped:
        for item in task.detection_items:
            zipped.write(item.origin_file, os.path.basename(item.origin_file))
            zipped.write(item.predict_file, os.path.basename(item.predict_file))
    return zip_bytes_io
