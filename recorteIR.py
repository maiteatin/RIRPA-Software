import numpy as np


def recorte(data):
    """Function used to split an impulse response from its maximum to its ending,
    resulting in a signal that only contains the slope of the IR and eliminates
    Harmonic distortion components of an IR obtained from a sine sweep recording.
    INPUT:
        data: IR one-dimensional vector signal"""

    in_max = np.where(abs(data) == np.max(abs(data)))[0]  # Windows signal from its maximum onwards.
    in_max = int(in_max[0])
    data = data[(in_max)+5:]
    return data

# import soundfile as sf
# import matplotlib.pyplot as plt
# data, fs = sf.read('RIR_App\IR_3.wav')
#
# data2 = recorte(data)
#
# plt.plot(data)
# plt.plot(data2)
# plt.show()