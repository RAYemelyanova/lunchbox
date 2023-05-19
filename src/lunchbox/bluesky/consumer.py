from pathlib import Path
from typing import Any, Callable, Dict, Optional


class Consumer:
    """Consumes bluesky documents.

    Stores information about resource and datum ids to keep track of files.
    """

    def __init__(self, executable: Callable[..., None]) -> None:
        self.executable: Callable[..., None] = executable
        self.resource_id: Optional[str] = None
        self.datum_id: Optional[str] = None
        self.datum_kwargs: Optional[Dict[str, Any]] = None
        self.filepath: Optional[Path] = None

    def __call__(self, name: str, doc: Dict[str, Any]) -> None:
        # if it's a resource doc, get the id...
        if name == "resource":
            root = str(doc.get("root"))
            filename = str(doc.get("resource_path"))

            self.filepath = Path(root) / filename
            self.resource_id = doc.get("uid")

        elif name == "datum":
            if doc["resource"] == self.resource_id:
                self.datum_id = doc.get("datum_id")
                self.datum_kwargs = doc.get("datum_kwargs")

        elif name == "event":
            data: Optional[Dict[str, Any]] = doc.get("data")

            if data and data.get("value") == self.datum_id:
                kwargs: Dict[str, Any] = (
                    self.datum_kwargs if self.datum_kwargs is not None else {}
                )

                self.executable(**kwargs)
