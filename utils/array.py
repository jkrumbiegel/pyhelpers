import numpy as np


def get_circle_coords(n, radius=1):

    angles = np.linspace(0, 360 - (360 / n), n) / 180 * np.pi
    coords = np.vstack((np.cos(angles) * radius, np.sin(angles) * radius)).T

    return coords
