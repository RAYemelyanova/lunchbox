import cv2
import numpy as np


def calibrate(image, distance=0.1):
    """Calibrate the image to work out the length along each pixel.

    For this to work, the input image must have two rectangular black blocks, spaced
    some distance apart, which by default is 10 cm or 0.1 metres.
    """
    masked = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
    no_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        cv2.bitwise_not(masked[1]).astype("uint8"), 4, cv2.CV_32S
    )

    assert no_labels >= 3, "Did not find at least 3 labels!"

    no_of_pixels = np.sqrt(sum((centroids[1] - centroids[2]) ** 2))

    return distance / no_of_pixels
