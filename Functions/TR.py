import numpy as np
from Functions.leastsquares import leastsquares


def TR(y, fs):
    """TR calculates T20, T30 and EDT parameters given a smoothed energy response "y" and its samplerate "fs" """
    t = np.arange(0, len(y) / fs, 1 / fs)

    i_max = np.where(y == max(y))                               # Finds maximum of input vector
    y = y[int(i_max[0][0]):]
    i_edt = np.where((y <= max(y) - 1) & (y > (max(y) - 10)))   # Index of values between 0 and -10 dB (Note: -1 to -10 dB interval used for calculations of EDT)
    i_20 = np.where((y <= max(y) - 5) & (y > (max(y) - 25)))    # Index of values between -5 and -25 dB
    i_30 = np.where((y <= max(y) - 5) & (y > (max(y) - 35)))    # Index of values between -5 and -35 dB

    t_edt = t[i_edt]
    t_20 = t[i_20]
    t_30 = t[i_30]

    y_edt = y[i_edt]
    y_t20 = y[i_20]
    y_t30 = y[i_30]

    m_edt, c_edt, f_edt = leastsquares(t_edt, y_edt)            #leastsquares function used to find slope intercept and line of each parameter
    m_t20, c_t20, f_t20 = leastsquares(t_20, y_t20)
    m_t30, c_t30, f_t30 = leastsquares(t_30, y_t30)

    EDT = -60 / m_edt                                         # EDT, T20 and T30 calculations
    T20 = -60 / m_t20
    T30 = -60 / m_t30

    return EDT, T20, T30


