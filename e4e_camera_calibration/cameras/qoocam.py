from pathlib import Path

import cv2
import numpy as np

from cameras.stereo_camera import StereoCamera


class QoocamEgoStereoCamera(StereoCamera):
    def __init__(self, **kwargs) -> None:
        super().__init__(manufacturer="Qoocam", model="Ego", **kwargs)

    @property
    def number_of_sensors(self) -> int:
        return 2

    def _load_image(self, file_path: str):
        return cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)

    def _preprocess_image(self, image: np.ndarray):
        _, width, _ = image.shape

        left = image[:, : int(width / 2), :]
        right = image[:, int(width / 2) :, :]

        return left, right

    def _process_directory(self, file_path: str):
        files = [str(p) for p in Path(file_path).iterdir() if p.is_file()]
        files.sort()
        return files
