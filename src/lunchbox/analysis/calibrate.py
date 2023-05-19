import cv2
import numpy as np


def calibrate(image, post_it_size_m=0.076) -> float:
    # 1. take the green only,
    # 2. blur and mask,
    # 3. count those pixels...
    total_i, total_j, _ = image.shape

    def percent_of_idx(idx, percent):
        return slice(int(idx * percent), -int(idx * percent))

    reduced_image = image[
        percent_of_idx(total_i, 0.25), percent_of_idx(total_j, 0.25), 0
    ]

    blurred = cv2.GaussianBlur(reduced_image, (3, 3), 0)
    threshold = blurred.min() + (2 * (blurred.max() - blurred.min()) / 5)
    masked = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)

    no_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        masked[1].astype("uint8"), 4, cv2.CV_32S
    )
    post_it_pixels = np.sort(stats[:, -1])[-2]  # 2nd largest area.

    return np.sqrt((post_it_size_m**2) / post_it_pixels)
