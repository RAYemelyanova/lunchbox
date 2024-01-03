from typing import Any, Dict, Optional

import numpy as np
import numpy.typing as npt
from ophyd import SignalRO
from picamera2 import Picamera2


class Camera(SignalRO):
    _controls = {
        "Contrast": 2,
        "ExposureTime": 100000,
        "AnalogueGain": 1.0,
        "NoiseReductionMode": 1,
        "AwbEnable": True,
        "AwbMode": 3,
    }

    def __init__(self, **kwargs) -> None:
        self.camera: Optional[Picamera2] = None
        super().__init__(**kwargs)

    @property
    def controls(self) -> Dict[str, Any]:
        return self._controls

    @controls.setter
    def controls(self, value: Dict[str, Any]) -> None:
        self._controls = value
        self.camera.set_controls(value)

    def start(self):
        self.camera = Picamera2()
        self.camera.configure(
            self.camera.create_still_configuration(
                {"size": (800, 600)}, controls=self.controls
            )
        )
        self.camera.start()

    def stop(self):
        self.camera.close()
        self.camera = None

    def get(self) -> npt.NDArray[np.uint8]:
        request = self.camera.capture_request(flush=True)
        array = request.make_array("main")
        request.release()
        return array
