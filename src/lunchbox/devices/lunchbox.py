import time
from datetime import datetime
from typing import Dict, List

from bluesky.protocols import Descriptor, Reading, SyncOrAsync
from ophyd import Component, Device, EpicsSignal

from .camera import Camera


class LunchBox(Device):
    camera = Component(Camera)
    servo = Component(
        EpicsSignal, read_pv="LUNCHBOX:SERVO:RBV", write_pv="LUNCHBOX:SERVO"
    )
    led = Component(
        EpicsSignal,
        read_pv="LUNCHBOX:LED:RBV",
        write_pv="LUNCHBOX:LED",
        put_complete=True,
    )

    def stage(self) -> List["LunchBox"]:
        self.servo.set(0.0)
        self.led.set(1.0)
        self.camera.create()
        return [self]

    def unstage(self) -> List["LunchBox"]:
        self.led.set(0.0)
        self.camera.delete()
        return [self]

    def read(self) -> SyncOrAsync[Dict[str, Reading]]:
        image = self.camera.get()
        return {
            "value": Reading(
                value=image,
                timestamp=time.mktime(datetime.now().timetuple()),
            )
        }

    def describe(self) -> SyncOrAsync[Dict[str, Descriptor]]:
        return {"value": Descriptor(source="cv2 camera", dtype="array", shape=[])}
