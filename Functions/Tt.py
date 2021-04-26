import numpy as np
from Functions.recorteIR import recorte
from Functions.lundeby import lundeby
from Functions.schroeder import schroeder
from Functions.chu import chuCompensation
from Functions.medianf import medianf
import sys
from Functions.leastsquares import leastsquares


def TtEDTt(ir, fs, smoothing, noiseComp, medianwindow):
    """ transition time (Tt) of a RIR is defined as the instant when the cumulative energy reaches 99% of the total
    energy. """
    ir = ir[int(5e-3 * fs):]  # Disregard first 5 ms after direct sound
    ir = recorte(ir)
    index = np.where(np.cumsum(ir ** 2) <= 0.99 * np.sum(ir ** 2))[0][-1]  # finds every index where the cumulative
    # sum of the energy is less than or equal to 99% of the total energy and then returns only its last index
    Tt = index / fs

    # ir = ir[:index]  # IR after windowing
    ir = ir / max(ir)
    ir **= 2
    if smoothing == 0:  # smoothing is 0 for Schroeder integration smoothing, and 1 for moving median filter smoothing
        if noiseComp == 0:  # indicates no compensation used
            sch = schroeder(ir, len(ir), 0, 0)
        if noiseComp == 1:  # indicates Lundeby's compensation
            t, C = lundeby(ir, fs, 0.01)
            sch = schroeder(ir, t, C, 0)
        if noiseComp == 2:  # indicates Chu's compensation
            rms = chuCompensation(ir)
            sch = schroeder(ir, len(ir), 0, rms)
    if smoothing == 1:
        sch = medianf(ir, medianwindow)
    sch = 10 * np.log10(sch / max(sch) + sys.float_info.epsilon)
    sch = sch[:index]  # IR after windowing

    t_Tt = np.arange(0, len(sch) / fs, 1/fs)
    m_EDTt, c_EDTt, f_EDTt = leastsquares(t_Tt, sch)
    EDTt = -60/m_EDTt

    return Tt, EDTt


