import numpy as np
import math
from Functions.leastsquares import leastsquares


def lundeby(y, Fs, Ts):
    """Given IR response "y" and samplerate "Fs" function returns upper integration limit of
    Schroeder's integral. Window length in ms "Ts" indicates window sized of the initial averaging of the input signal,
    Luneby recommends this value to be in the 10 - 50 ms range."""

    y_power = y
    y_promedio = np.zeros(int(len(y) / Fs / Ts))
    eje_tiempo = np.zeros(int(len(y) / Fs / Ts))

    t = math.floor(len(y_power) / Fs / Ts)
    v = math.floor(len(y_power) / t)

    for i in range(0, t):
        y_promedio[i] = sum(y_power[i * v:(i + 1) * v]) / v
        eje_tiempo[i] = math.ceil(v / 2) + (i * v)

    # First estimate of the noise level determined from the energy present in the last 10% of input signal
    ruido_dB = 10 * np.log10(
        sum(y_power[round(0.9 * len(y_power)):len(y_power)]) / (0.1 * len(y_power)) / max(y_power))
    y_promediodB = 10 * np.log10(y_promedio / max(y_power))

    # Decay slope is estimated from a linear regression between the time interval that contains the maximum of the
    # input signal (0 dB) and the first interval 10 dB above the initial noise level
    r = int(max(np.argwhere(y_promediodB > ruido_dB + 10)))
    m, c, rectacuadmin = leastsquares(eje_tiempo[0:r], y_promediodB[0:r])
    cruce = (ruido_dB - c) / m

    if ruido_dB > -20:  # Insufficient S/N ratio to perform Lundeby
        punto = len(y_power)
        C = None
    else:

        # Begin Luneby's iterations
        error = 1
        INTMAX = 25
        veces = 1
        while error > 0.0001 and veces <= INTMAX:

            # Calculates new time intervals for median, with aprox. p-steps per 10 dB
            p = 10  # Number of steps every 10 dB
            delta = abs(10 / m)  # Number of samples for the 10 dB decay slope
            v = math.floor(delta / p)  # Median calculation window
            if (cruce - delta) > len(y_power):
                t = math.floor(len(y_power) / v)
            else:
                t = math.floor(len(y_power[0:round(cruce - delta)]) / v)
            if t < 2:
                t = 2

            media = np.zeros(t)
            eje_tiempo = np.zeros(t)
            for i in range(0, t):
                media[i] = sum(y_power[i * v:(i + 1) * v]) / len(y_power[i * v:(i + 1) * v])
                eje_tiempo[i] = math.ceil(v / 2) + (i * v)
            mediadB = 10 * np.log10(media / max(y_power))
            m, c, rectacuadmin = leastsquares(eje_tiempo, mediadB)

            # New median of the noise energy calculated, starting from the point of the decay line 10 dB under the cross-point
            noise = y_power[(round(abs(cruce + delta))):]
            if len(noise) < round(0.1 * len(y_power)):
                noise = y_power[round(0.9 * len(y_power)):]
            rms_dB = 10 * np.log10(sum(noise) / len(noise) / max(y_power))

            # New cross-point
            error = abs(cruce - (rms_dB - c) / m) / cruce
            cruce = round((rms_dB - c) / m)
            veces += 1
    # output
    if cruce > len(y_power):
        punto = len(y_power)
    else:
        punto = cruce
    C = max(y_power) * 10 ** (c / 10) * math.exp(m / 10 / np.log10(math.exp(1)) * cruce) / (
                -m / 10 / np.log10(math.exp(1)))
    return punto, C
