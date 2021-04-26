import numpy as np


def IACC(IR_L, IR_R, fs):
    """Calculates IACC parameters from binaural impulse response as
    defined by ISO 3382:2001. 
    Inputs:
    - IR_L: Impulse response in left channel.
    - IR_R: Impulse response in right channel.
    - fs: Sampling frequency of IR signals.
    Outputs:
    - IACCearly: 0 - 80 ms.
    - IACClate: 80 - inf ms.
    - IACCall: 0 - inf ms.
    """
    IR_L = np.array(IR_L)
    IR_R = np.array(IR_R)
    t80 = np.int64(0.08*fs)  # Index of signal value at 80 ms
    IACFearly = np.correlate(IR_L[0:t80], IR_R[0:t80])/(np.sqrt(np.sum(IR_L[0:t80]**2)*(np.sum(IR_R[0:t80]**2))))
    IACFlate = np.correlate(IR_L[t80:], IR_R[t80:])/(np.sqrt(np.sum(IR_L[t80:]**2)*(np.sum(IR_R[t80:]**2))))
    IACFall = np.correlate(IR_L, IR_R)/(np.sqrt(np.sum(IR_L**2)*(np.sum(IR_R**2))))
    IACCearly = np.max(np.abs(IACFearly))
    IACClate = np.max(np.abs(IACFlate))
    IACCall = np.max(np.abs(IACFall))
    return IACCearly, IACClate, IACCall
