from math import degrees

import numpy as np


def find_theta(
    spot_distance: float,
    grating_distance: float,
) -> float:
    """Theta, alpha in degrees. wavelength in metres.

    spot distance is the distance between central spot and nth order spot in metres.
    grating distance is distance between diffraction grating and wall.

    Returns theta
    """

    theta = np.arctan(spot_distance / grating_distance)
    return degrees(theta)
