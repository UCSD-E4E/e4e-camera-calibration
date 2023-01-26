from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from typing import List

import numpy as np


class Camera(ABC):
    def __init__(
        self,
        name: str = None,
        manufacturer: str = None,
        model: str = None,
        serial_number: str = None,
    ) -> None:
        super().__init__()

        self._image_files: List[str] = None
        self._image_files_idx = 0
        self._name = name
        self._manufacturer = manufacturer
        self._model = model
        self._serial_number = serial_number

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def model(self):
        return self._model

    @property
    def name(self):
        return self._name

    @abstractproperty
    def number_of_sensors(self) -> int:
        raise NotImplementedError()

    @property
    def serial_number(self):
        return self._serial_number

    def load(self, file_path: str):
        path = Path(file_path)

        if path.is_dir():
            self._image_files = self._process_directory(file_path)
            self._image_files_idx = 0
        else:
            raise NotImplementedError()

    @abstractmethod
    def _load_image(self, file_path: str):
        raise NotImplementedError()

    @abstractmethod
    def _preprocess_image(self, image: np.ndarray):
        raise NotImplementedError()

    @abstractmethod
    def _process_directory(self, file_path: str):
        raise NotImplementedError()

    def __iter__(self):
        return self

    def __next__(self):
        if self._image_files_idx < len(self._image_files):
            file = self._image_files[self._image_files_idx]
            self._image_files_idx += 1

            image = self._load_image(file)

            return self._preprocess_image(image)

        raise StopIteration
