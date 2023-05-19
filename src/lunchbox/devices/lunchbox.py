import time
import uuid
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

import h5py
from bluesky.protocols import Asset, Datum, Descriptor, Reading, Status, SyncOrAsync
from ophyd import Component, Device, DeviceStatus, EpicsSignal, EpicsSignalRO, Signal

from lunchbox.analysis.calibrate import calibrate
from lunchbox.devices.camera import Camera

INF = 100


class LunchBox(Device):
    camera = Component(Camera)
    servo_read = Component(EpicsSignalRO, read_pv="LUNCHBOX:SERVO:RBV")
    led = Component(
        EpicsSignal,
        read_pv="LUNCHBOX:LED:RBV",
        write_pv="LUNCHBOX:LED",
        put_complete=True,
    )
    directory = Component(Signal, kind="config")
    filename = Component(Signal, kind="config")
    count = Component(Signal)
    pixel_width = Component(Signal, kind="config")
    grating_distance = Component(Signal, kind="config")

    def __init__(self, *args, **kwargs) -> None:
        super(LunchBox, self).__init__(*args, **kwargs)
        self.file: Optional[h5py.File] = None
        self.resource_path: Optional[str] = None
        self._asset_docs_cache: deque = deque()
        self.filestore_spec: str = "HDF5"
        self.path_semantics: str = "posix"
        self.angles: List[Any] = []

    def resource_factory(
        self,
        resource_kwargs,
    ):
        resource_uid = str(uuid.uuid4())

        assert self.resource_path is not None, "please set resource path!"
        resource_doc = {
            "spec": self.filestore_spec,
            "root": self.directory.get(),
            "resource_path": self.resource_path,
            "resource_kwargs": resource_kwargs,
            "path_semantics": self.path_semantics,
            "uid": resource_uid,
        }

        def datum_factory(datum_kwargs):
            i = self.count.get()
            datum_id = "{}/{}".format(resource_uid, i)
            return Datum(
                resource=resource_uid, datum_id=datum_id, datum_kwargs=datum_kwargs
            )

        return resource_doc, datum_factory

    def stage(self) -> List["LunchBox"]:
        self.resource_path = f"{self.filename.get()}.h5"

        self.file = h5py.File(
            str(Path(self.directory.get()) / self.resource_path),
            "w",
            libver="latest",
        )
        resource, self.datum_factory = self.resource_factory({})

        self.camera.create()

        self.pixel_width.set(calibrate(self.camera.get()))

        self.count.set(0)
        self.led.set(1.0)

        self._asset_docs_cache.append(("resource", resource))
        return [self]

    def unstage(self) -> List["LunchBox"]:
        self.led.set(0.0)
        self.camera.delete()

        h5file = self.file
        assert h5file is not None, "stage not run"

        final_count = self.count.get()
        h5file.attrs["number_of_scans"] = final_count
        h5file.close()
        return [self]

    def trigger(self) -> Status:
        status = DeviceStatus(self)
        self.led.set(0.0).wait()
        background = self.camera.get()
        count = int(self.count.get())

        self.count.set(count + 1).wait()

        h5file = self.file
        assert h5file is not None, "stage not run"
        if count == 0:
            h5file.create_dataset(
                "/images", shape=(INF, *background.shape), dtype="uint8"
            )
            h5file.create_dataset(
                "/backgrounds", shape=(INF, *background.shape), dtype="uint8"
            )
            h5file.swmr_mode = True

        self.led.set(1.0).wait()
        image = self.camera.get()

        img_data = h5file["/images"]
        bkg_data = h5file["/backgrounds"]

        if isinstance(img_data, h5py.Dataset):
            img_data[count] = image

        if isinstance(bkg_data, h5py.Dataset):
            bkg_data[count] = background

        status.set_finished()
        return status

    def read(self) -> SyncOrAsync[Dict[str, Reading]]:
        datum = self.datum_factory({"location": self.count.get() - 1})
        self._asset_docs_cache.append(("datum", datum))
        return {
            "value": Reading(
                value=datum["datum_id"],
                timestamp=time.mktime(datetime.now().timetuple()),
            )
        }

    def describe(self) -> SyncOrAsync[Dict[str, Descriptor]]:
        return {"value": Descriptor(source="cv2 camera", dtype="string", shape=[])}

    def collect_asset_docs(self) -> Iterator[Asset]:
        items = list(self._asset_docs_cache)
        self._asset_docs_cache.clear()
        for item in items:
            yield item
