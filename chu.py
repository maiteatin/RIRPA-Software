import numpy as np


# Chu Compensation for handling background noise by subtracting
# its mean squared value (RMS) from the original squared signal before
# performing integration.

def chuCompensation(y):
    """Calculates the mean squared value of the last x% of the signal
    where it is assumed that the response has vanished and only
    the background noise remains.
    y must be a numpy array"""

    x = 10  # Percentage of signal over which the RMS value will be obtained.
    y_len = len(y)
    y_start = int(np.round((1 - x / 100) * y_len))
    y_trimmed = y[y_start:]  # Trims the y signal keeping only the last x% of itself as specified.
    # rms = np.mean(y_trimmed**2) # Calculates the mean squared value
    rms = np.mean(y_trimmed)  # Calculates the mean squared value
    return rms

