import numpy as np
from scipy.ndimage import median_filter


def medianf(y, m):
    """medianf calculates de moving median average of "y" input signal over an "m" sized window.
    median_filter() function of the scipy library is implemented"""
    env = np.zeros_like(y)
    for i in range(len(y)):
        env[i] = median_filter(y[i], m)
    return env

