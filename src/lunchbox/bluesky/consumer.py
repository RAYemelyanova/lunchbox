from pathlib import Path
from typing import Any, Dict, Optional

from lunchbox.analysis.spotfinder import SpotFinder


class Consumer:
    """Consumes bluesky documents.

    Stores information about resource and datum ids to keep track of files.
    """

    def __init__(self) -> None:
        self.spot_finder: Optional[SpotFinder] = None
        self.resource_id: Optional[str] = None
        self.datum_id: Optional[str] = None
        self.datum_kwargs: Optional[Dict[str, Any]] = None
        self.filepath: Optional[Path] = None
        self.pixel_width: Optional[float] = None
        self.grating_distance: Optional[float] = None

    def __call__(self, name: str, doc: Dict[str, Any]) -> None:
        # if it's a resource doc, get the id...
        if name == "descriptor":
            config = doc["configuration"]["lunchbox"]["data"]

            assert config, "wrong document schema"
            self.pixel_width = float(config["lunchbox_pixel_width"])
            self.grating_distance = float(config["lunchbox_grating_distance"])

        if name == "resource":
            root = str(doc.get("root"))
            filename = str(doc.get("resource_path"))
            filepath = Path(root) / Path(filename)

            self.resource_id = doc.get("uid")

            assert self.pixel_width and self.grating_distance, "descriptor not found"
            self.spot_finder = SpotFinder(
                filepath, self.pixel_width, self.grating_distance
            )

        elif name == "datum":
            if doc["resource"] == self.resource_id:
                self.datum_id = doc.get("datum_id")
                self.datum_kwargs = doc.get("datum_kwargs")

        elif name == "event":
            data: Optional[Dict[str, Any]] = doc.get("data")
            assert self.spot_finder
            if data and data.get("value") == self.datum_id:
                kwargs: Dict[str, Any] = (
                    self.datum_kwargs if self.datum_kwargs is not None else {}
                )
                angle = data.get("LUNCHBOX:SERVO:RBV")
                if angle:
                    self.spot_finder(float(angle), **kwargs)
