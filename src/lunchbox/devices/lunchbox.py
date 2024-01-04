from time import time
from typing import Dict, Optional

import numpy as np
import numpy.typing as npt
from bluesky.protocols import Reading
from event_model.documents.event_descriptor import DataKey
from ophyd import Component, Device, DeviceStatus, EpicsSignal, Signal

from lunchbox.analysis import calibrate, euclidean_distance, get_spot_coordinates
from lunchbox.devices.camera import Camera

CAMERA_TIMEOUT = 10.0


class LunchBox(Device):
    camera = Component(Camera)
    laser = Component(
        EpicsSignal,
        read_pv="LUNCHBOX:LASER:RBV",
        write_pv="LUNCHBOX:LASER",
        put_complete=True,
    )

    count = Component(Signal)

    def __init__(self, calibration_distance, threshold, name) -> None:
        super().__init__(name=name)
        self.calibration_distance = calibration_distance
        self.threshold = threshold
        self.background_image: Optional[npt.NDArray] = None
        self.image: Optional[npt.NDArray] = None
        self.m_per_pixel: Optional[float] = None

    def stage(self):
        self.count.set(0)
        self.camera.start()
        self.m_per_pixel = calibrate(
            self.camera.get()[..., 1], distance=self.calibration_distance
        )

    def unstage(self):
        final_count = self.count.get()
        print("final count is: ", final_count)
        self.camera.stop()
        self.laser.set(0)

    def trigger(self) -> DeviceStatus:
        status = DeviceStatus(device=self, timeout=CAMERA_TIMEOUT)

        try:
            self.laser.set(0).wait()
            self.background_image = self.camera.get()

            self.laser.set(100).wait()
            self.image = self.camera.get()

            self.count.set(self.count.get() + 1)
        except Exception as exc:
            status.set_exception(exc)
        finally:
            status.set_finished()

        return status

    def read(self) -> Dict[str, Reading]:
        return {
            self.name: Reading(
                value=self.spot_distances_from_middle(), timestamp=time()
            )
        }

    def describe(self) -> Dict[str, DataKey]:
        return {self.name: DataKey(dtype="array", source="LUNCHBOX", shape=[2])}

    def spot_distances_from_middle(self):
        coords = get_spot_coordinates(self.background_image, self.image, self.threshold)
        sorted_coords = np.sort(coords, axis=0)
        return [
            euclidean_distance(sorted_coords[i], sorted_coords[1]) * self.m_per_pixel
            for i in [0, 2]
        ]
