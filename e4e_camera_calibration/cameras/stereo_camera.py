from abc import ABC
from cameras.camera import Camera


class StereoCamera(Camera, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def number_of_sensors(self) -> int:
        return 2
