import numpy as np
from scipy import signal


def iss(ch, sweep, f1, f2, d, fs, tipo):
    """Function generates an inverse filter given a linear or logarithmic sine sweep between the specified input frequencies
    and sweep duration. Convolution between the sweep and its inverse gives IR response.
    INPUTS:
        f1: initial frequency of sweep [Hz]
        f2: final frequency of sweep [Hz]
        d: sweep length [s]
        fs: sample rate [Hz]
        tipo: linear or log, type sweep (tipo = 0 and tipo = 1 respectably) """

    t = np.arange(0, round(d), 1 / fs)
    w1 = 2 * np.pi * f1
    w2 = 2 * np.pi * f2

    if tipo == 1:  # Inverse filter for log sine sweep

        K = (w1 / np.log(w2 / w1)) * d
        L = d / np.log(w2 / w1)
        y = np.sin(K * (np.exp(t / L) - 1))  # Log Sine Sweep

        w = (K / L) * np.exp(t / L)
        m = w1 / w

        u = m * np.flip(y)
        u = u / max(abs(u))  # Inverse Log Sine Sweep

        lenDiff = len(sweep) - len(u)

        u = np.pad(u, (0, lenDiff))

    else:  # Inverse filter for linear sine sweep

        wl = w1 + ((w2 - w1) / d) * t

        y = np.sin(w1 + ((w2 - w1) / d) * (t ** 2) / 2)  # Linear Sine Sweep
        u = np.sin(w1 + ((w2 - w1) / d) * ((np.flip(t)) ** 2) / 2)  # Inverse Linear Sine Sweep
        u = u / max(abs(u))

    if ch == 1:
        ir = signal.fftconvolve(sweep, u)
    else:
        ir_L = signal.fftconvolve(sweep[:, 0], u)
        ir_R = signal.fftconvolve(sweep[:, 1], u)

        ir = np.zeros((len(ir_R), 2))
        ir[:, 0] = ir_L
        ir[:, 1] = ir_R

    return ir

# PRUEBAS
# import matplotlib.pyplot as plt
# from audioRead import audioRead
# data, samplerate, path, duration, frames, channels = audioRead('P1_R.wav')
#
# f1 = 60
# f2 = 20000
# d = 20
# fs = samplerate
# tipo = 1
# ch = channels
#
# ir = iss(ch, data, f1, f2, d, fs, tipo)
#
#
# # u_fft = np.fft.rfft(u)
# # y_fft = np.fft.rfft(y)
# #
# # ir = abs(y_fft) * abs(u_fft)
# # ir = np.fft.ifft(ir)
#
#
# plt.figure()
# plt.plot(ir)
# plt.show()
#
