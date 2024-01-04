import numpy as np


def euclidean_distance(coord_1, coord_2):
    return np.sqrt(sum((coord_1 - coord_2) ** 2))
