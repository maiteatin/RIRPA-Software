import numpy as np


def cParameters(IR, fs):
    """Calculates C50 and C80 (a.k.a. "clarity") parameters and Ts (Centre time) from impulse response data.
    # Sampling frequency (fs) must be specified.
    # Based on UNE-EN ISO 3382:2001.
    # Centre Time (Ts) is the centre of gravity of the squared impulse response. It is the perceived
    # balance of the room between clarity and reverberation."""
    t50 = np.int64(0.05*fs)  # Index of signal value at 50 ms
    t80 = np.int64(0.08*fs)  # Index of signal value at 80 ms
    y50_num = IR[0:t50]
    y50_den = IR[t50:]
    y80_num = IR[0:t80]
    y80_den = IR[t80:]
    C50 = 10*np.log10((np.sum(y50_num))/(np.sum(y50_den)))
    C80 = 10*np.log10((np.sum(y80_num))/(np.sum(y80_den)))
    # D50 = (np.sum(y50_num**2))/(np.sum(IR**2))
    t = np.arange(0, len(IR))/fs
    Ts = (np.sum(t * IR) / np.sum(IR))                # x1000 in milliseconds
    return C50, C80, Ts
