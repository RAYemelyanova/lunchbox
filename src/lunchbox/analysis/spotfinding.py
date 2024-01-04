import cv2
import numpy as np


def get_spot_coordinates(background_image, image, threshold):
    """Finds the x,y location of diffraction spots in an image.

    This can be calculated by finding the difference between a background image (sans
    spots) and image (with spots) taken close together.
    """

    image_delta = image[..., 0].astype("int16") - background_image[..., 0].astype(
        "int16"
    )
    image_delta[image_delta < 0] = 0
    masked = cv2.threshold(image_delta, threshold, 1, cv2.THRESH_BINARY)
    no_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        masked[1].astype("uint8"), 4, cv2.CV_32S
    )

    # sort the labels by area, taking the biggest ones first.
    sorted_indices = np.argsort(stats[:, -1])
    return centroids[sorted_indices][
        -4:-1
    ]  # get the three biggest things, excluding the background.
