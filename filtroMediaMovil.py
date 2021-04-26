import numpy as np


def filtromediamovil(x, N):
    """
    Filters x, one-dimensional input vector with an N sized moving average filter window
    """
    out = np.zeros([x.shape[0], x.shape[1]-N+1])
    for i in range(out.shape[0]):
        array = np.insert(x[i], 0, 0)  # converts input to numpy.float64 type
        cumsum = np.cumsum(array)  # cumsum of array
        out[i] = np.array((cumsum[N:] - cumsum[:-N]) / float(N))  # rest and averaging
    return out
