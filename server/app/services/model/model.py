import json
import os
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

from app.config import get_settings
from app.constants import DetectionItemType
from app.services.metaclasses import Singleton


class YOLOWrapper(metaclass=Singleton):
    def __init__(self, path: str = "./weights/yolov8s.pt", conf: float = 0.25, iou: float = 0.7):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(path).to(self.device)
        self.conf = conf
        self.iou = iou
        self.classes = self.model.names
        self.media_path = Path(get_settings().MEDIA_PATH)
        self.functions = {
            DetectionItemType.IMAGE: self.run_detection_images,
            DetectionItemType.VIDEO: self.run_detection_videos,
        }

    def save_image(self, final_dict: list, dir_save: str, boxes: dict) -> list[dict]:
        filename = f"predict_{os.path.basename(final_dict['filename'])}"
        path = os.path.join(self.media_path, dir_save, filename)
        final_dict["result_path"] = path
        annotator = Annotator(cv2.cvtColor(final_dict['image'], cv2.COLOR_BGR2RGB))
        for item in boxes:
            text = item['name']
            box = item["box"]
            bbox = [box['x1'], box['y1'], box['x2'], box['y2']]
            annotator.box_label(bbox, text, color=colors(item['class'], True))
        pixels = annotator.result()
        plt.imsave(path, pixels)
        final_dict.pop("image")
        return final_dict

    def convert_images_to_video(self, images: list[np.ndarray], filename: str, fps: int = 24, codec: str = "mp4v"):
        img = images[0]

        height = img.shape[0]
        width = img.shape[1]

        fourcc = cv2.VideoWriter_fourcc(*codec)
        video = cv2.VideoWriter(filename, fourcc, fps, (width, height))

        for img in images:
            video.write(img)

        video.release()
        return video

    def run_detection_images(
        self,
        filename: str,
        dir_save: str
    ) -> dict:
        result = self.model.predict(
            filename,
            conf=self.conf,
            iou=self.iou,
            verbose=False,
        )[0]
        boxes = json.loads(result.tojson())
        classes = []
        for item in boxes:
            classes.append(item["name"])
        
        final_dict = {
            'filename': filename,
            'classes': classes,
            'image': result.orig_img,
        }
        return self.save_image(final_dict, dir_save, boxes)

    def run_detection_videos(
        self,
        filename: str,
        dir_save: str,
    ) -> dict:
        capture = cv2.VideoCapture(filename=str(filename))
        new_filename = f"predict_{os.path.basename(filename)}"
        file_name, file_extension = os.path.splitext(new_filename)
        path = os.path.join(self.media_path, dir_save, f"{file_name}{file_extension}")
        webm_path = os.path.join(self.media_path, dir_save, f"{file_name}.webm")

        lst_images = []

        count_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = capture.get(cv2.CAP_PROP_FPS)

        classes = set()
        while capture.isOpened() and count_frames >= -1:
            success, frame = capture.read()
            if success:
                result = self.model(
                    frame,
                    conf=self.conf,
                    iou=self.iou,
                    verbose=False,
                )[0]
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), colors(int(box.cls), True), 2)
                    cls = int(box.cls[0])
                    classes.add(self.classes[cls])
                    cv2.putText(frame, self.classes[cls], (max(0, x1), max(35, y1)), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), thickness=1)
            lst_images.append(frame)
            count_frames -= 1

        self.convert_images_to_video(lst_images, path, fps=fps)
        self.convert_images_to_video(lst_images, webm_path, fps=fps, codec="vp80")
        capture.release()

        final_dict = {
            'filename': filename,
            'classes': list(classes),
            'result_path': path
        }
        return final_dict
