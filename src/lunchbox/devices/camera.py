from typing import Optional

import numpy as np
import numpy.typing as npt
from ophyd import SignalRO
from picamera import PiCamera

FULL_H = 1920
FULL_W = 2560


class Camera(SignalRO):
    def __init__(self, **kwargs) -> None:
        self.camera: Optional[PiCamera] = None
        super(Camera, self).__init__(**kwargs)

    def create(self):
        assert self.camera is None, "camera already exists"
        self.camera = PiCamera(resolution=(FULL_W, FULL_H))
        self.camera.framerate = 32
        self.camera.shutter_speed = int((1 / 32) * 1e6)
        self.camera.iso = 120
        self.camera.zoom = (0.2, 0.1, 0.8, 0.8)

    def get(
        self,
    ) -> npt.NDArray[np.uint8]:
        image = np.empty((FULL_H, FULL_W, 3), dtype=np.uint8)
        assert self.camera, "cannot get image; camera has not been made."
        self.camera.capture(image, "rgb")
        return image

    def delete(self):
        assert self.camera, "there is no camera to delete"
        self.camera.close()
