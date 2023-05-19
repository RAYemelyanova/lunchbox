from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
import numpy.typing as npt
from h5py import Dataset, File

from lunchbox.analysis.find_theta import find_theta


@dataclass
class FileSlice:
    image: npt.NDArray[np.float64]
    background: npt.NDArray[np.float64]


class SpotFinder:
    """Finds distances between 0 and 1st order diffraction spots.

    This class should be initialised with calibration information like the
    meters per pixel, and grating distance.
    """

    filepath: Path
    m_per_pixel: float
    grating_distance: float
    plus_angles: List[float]
    minus_angles: List[float]
    servo_angles: List[float]
    file_info: Optional[FileSlice]

    def __init__(
        self, filepath: Path, m_per_pixel: float, grating_distance: float
    ) -> None:
        self.filepath = filepath
        self.m_per_pixel = m_per_pixel
        self.grating_distance = grating_distance
        self.plus_angles = []
        self.minus_angles = []
        self.servo_angles = []
        self.file_info = None

    def open_file(self, location: str) -> None:
        """Opens the file, and extracts the necessary information for a slice."""
        with File(str(self.filepath), "r", swmr=True, libver="latest") as file:
            image = file["/images"]
            background = file["/backgrounds"]

            if not isinstance(image, Dataset) or not isinstance(background, Dataset):
                raise Exception("Could not open dataset.")

            image_slice = np.array(image[int(location)])
            background_slice = np.array(background[int(location)])

        self.file_info = FileSlice(image=image_slice, background=background_slice)

    def find_spot_centres(self, lower_threshold: int = 15):
        """Finds the diffraction spot centres of the current image.

        With a 3.3v class 2 laser, you should only really get 3 spots. Either
        way this method should return the 3 largest spots observed by area.
        """
        assert self.file_info, "file not opened"
        image, background = self.file_info.image, self.file_info.background

        blurred_image = cv2.GaussianBlur(image, (15, 15), 0)[..., 0].astype("int16")
        blurred_background = cv2.GaussianBlur(background, (15, 15), 0)[..., 0].astype(
            "int16"
        )

        diff = blurred_image - blurred_background
        diff[diff < 0] = 0  # ignore negative values; these are noise.

        masked = cv2.threshold(diff, lower_threshold, 255, cv2.THRESH_BINARY)

        no_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            masked[1].astype("uint8"), 4, cv2.CV_32S
        )

        # filter out any labels which aren't in line with the centroid...

        # make sure to sort by area...
        sorted_indices = np.argsort(stats[:, -1])

        # returning only those centroids that aren't the background.
        # centroids[sorted_indices] will be sorted from smallest to biggest area.
        # last elem is background. 2nd to last is centroid.

        return centroids[sorted_indices][-4:-1]  # get the three biggest things

    def __call__(self, alpha: float, location: str = "") -> None:
        """calculates distances between diffraction spots for a given file.

        This method is designed to be called with each event document. It opens a
        specific location in the HDF5 file (corresponding to the data for this event)
        and uses the image of the diffraction spots as well as a background image to
        find where the spots are.
        """
        self.open_file(location)

        # an array of spots, increasing in area. last is centroid.
        spots = self.find_spot_centres()

        spot_orders: Dict[str, float] = {}
        assert spots.shape[0] <= 3, "more than 3 spots found. Something is wrong!"

        for spot in spots[:-1]:
            # only expecting to see 3 spots, at most.
            sign: str = "+" if spot[0] > spots[-1][0] else "-"

            distance_from_centroid: float = (
                np.sqrt((spot[0] - spots[-1][0]) ** 2 + (spot[1] - spots[-1][1]) ** 2)
                * self.m_per_pixel
            )

            spot_orders[sign] = distance_from_centroid

        self.servo_angles.append(alpha)

        for key, value in spot_orders.items():
            theta = find_theta(value, self.grating_distance)

            if key == "-":
                self.minus_angles.append(theta)
            elif key == "+":
                self.plus_angles.append(theta)
