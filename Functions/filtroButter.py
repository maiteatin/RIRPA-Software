import numpy as np
from scipy import signal


def filterButterBP(y, fs, division, rangef):
    """
    Pass-band Butterworth filter, 8th order, central frequencies given by "division"
    y = array to be filtered
    fs = sample rate
    division = 1 for 1/3 octave filtering and = 0 for 1/1 octave filtering
    """
    G = 2.0
    n = 3.0
    nyquistRate = fs / 2

    if division == 1:
        centerFrequency_Hz = np.array([25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315,
                                       400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150,
                                       4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000])
        if rangef:
            centerFrequency_Hz = centerFrequency_Hz[rangef[0]:rangef[1] + 1]

        # Superior and inferior limits of each central band
        factor = np.power(G, 1 / (2 * n))
        lowerCutoffFrequency_Hz = centerFrequency_Hz / factor
        upperCutoffFrequency_Hz = centerFrequency_Hz * factor
        if np.where(centerFrequency_Hz == 20000)[0]:
            upperCutoffFrequency_Hz[np.where(centerFrequency_Hz == 20000)[0]] = 22049
        filteredSignal = np.zeros((len(centerFrequency_Hz), len(y)))
    else:
        centerFrequency_Hz = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
        if rangef:
            centerFrequency_Hz = centerFrequency_Hz[rangef[0]:rangef[1] + 1]
        # Superior and inferior limits of each central band
        factor = np.sqrt(2)
        lowerCutoffFrequency_Hz = centerFrequency_Hz / factor
        upperCutoffFrequency_Hz = centerFrequency_Hz * factor
        if np.where(centerFrequency_Hz == 16000)[0]:
            upperCutoffFrequency_Hz[np.where(centerFrequency_Hz == 16000)[0]] = 22049
        filteredSignal = np.zeros((len(centerFrequency_Hz), len(y)))

    # Creation and application of the filter
    for lower, upper in zip(lowerCutoffFrequency_Hz, upperCutoffFrequency_Hz):  # IIR Butterworth Filter N-th order
        sos = signal.butter(N=8, Wn=np.array([lower,
                                              upper]) / nyquistRate, btype='bandpass', analog=False,
                            output='sos')

        # w, h = signal.sosfreqz(sos)  # Frequency response of filter

        #        plt.plot(w*(fs/(2*np.pi)), 20 * np.log10(abs(h)), 'b')          # Plot freq response

        index = np.where(lowerCutoffFrequency_Hz == lower)  # Finds index of iteration to store signal
        index = index[0]

        filteredSignal[index, :] = signal.sosfiltfilt(sos, y)  # Filters the input "y" signal

    return filteredSignal, centerFrequency_Hz
