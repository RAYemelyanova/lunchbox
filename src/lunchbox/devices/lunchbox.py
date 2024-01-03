from time import time
from typing import Dict

from bluesky.protocols import Reading
from event_model.documents.event_descriptor import DataKey
from ophyd import Component, Device, DeviceStatus, EpicsSignal, Signal

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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.latest_image = None

    def stage(self):
        self.count.set(0)
        self.camera.start()

    def unstage(self):
        final_count = self.count.get()
        print("final count is: ", final_count)
        self.camera.stop()

    def trigger(self) -> DeviceStatus:
        status = DeviceStatus(device=self, timeout=CAMERA_TIMEOUT)
        self.laser.set(100).wait()

        try:
            self.latest_image = self.camera.get()
            self.count.set(self.count.get() + 1)
        except Exception as exc:
            status.set_exception(exc)
        finally:
            status.set_finished()

        self.laser.set(0).wait()
        return status

    def read(self) -> Dict[str, Reading]:
        return {self.name: Reading(value=self.latest_image, timestamp=time())}

    def describe(self) -> Dict[str, DataKey]:
        return {
            self.name: DataKey(
                dtype="array",
                source="LUNCHBOX",
                shape=list(self.camera.camera.camera_config["main"]["size"])[::-1]
                + [3],
            )
        }
