import numpy as np
from tkinter import sys
from Functions.cParameters import cParameters
from Functions.filtroButter import filterButterBP
from Functions.schroeder import schroeder
from Functions.recorteIR import recorte
from Functions.lundeby import lundeby
from Functions.chu import chuCompensation
from Functions.TR import TR
from Functions.IACC import IACC as IACCf
from Functions.Tt import TtEDTt
from Functions.medianf import medianf


# calculateMain.py is the main processing script, where most other functions used to process the desired IR response
# are called.

def calculateMono(ir, fs, analysis, smoothing, noiseComp, medianwindow, rangef, *IACC):
    """Calculates single channel parameters for EDT, T20, T30, C50, C80, Ts, Tt and EDTt given the desired smoothing
    and filtering parameters. """

    ir = recorte(ir)  # Signal is windowed after IR sound.
    if len(ir) / fs > 15:
        ir = ir[0:int(15 * fs)]  # If the lenght of the resulting IR is over 15 seconds,
        # it is shortened to 15 seconds to avoid overly large data to be processed.

    irFilt2, centerFrequency_Hz = (filterButterBP(np.flip(ir), fs,
                                                  analysis, rangef))  # analysis is 0 for octave-band filtering and 1 for 1/3 octave band filtering
    irFilt2 = np.flip(irFilt2, 1)  # Time-reversed analysis. np.flip() used before and after filtering
    irFilt2 = np.vstack((irFilt2, ir))

    # irFilt2 = np.abs(hilbert(irFilt2))                      # Uncomment to use Hilbert smoothing
    ir_IACC = irFilt2  # ir_IACC variable stored for calculating IACC parameters if optional args input argument *IACC is passed.

    Tt = np.zeros(len(irFilt2))  # Tt and EDTt calculation
    EDTt = np.zeros(len(irFilt2))
    for i in range(len(irFilt2)):
        try:
            Tt[i], EDTt[i] = TtEDTt(irFilt2[i], fs, smoothing, noiseComp, medianwindow)
        except:
            print("Error detected while analyzing " + str(int(centerFrequency_Hz[
                                                                  i])) + " Hz octave or 1/3 octave band. Results will omit Tt and EDTt in this frequency band")

    max_h = np.zeros(irFilt2.shape[0])  # Normalization of signal
    for i in range(len(irFilt2)):
        max_h[i] = max(irFilt2[i])
        irFilt2[i] = irFilt2[i] / max_h[i]

    irFilt = irFilt2 ** 2

    # irFilt = np.zeros((len(irFilt2), int(len(irFilt2[0])*0.95)))  #Uncomment to discard last 5% of signal where filter ringing is sometimes present
    # for i in range(len(irFilt2)):
    #     irFilt[i] = irFilt2[i][0:int(len(irFilt2[i]) * 0.95)]

    if smoothing == 0:  # smoothing is 0 for Schroeder integration smoothing, and 1 for moving median filter smoothing
        if noiseComp == 0:  # indicates no compensation used
            sch = np.zeros_like(irFilt)
            for i in range(len(irFilt)):
                sch[i] = schroeder(irFilt[i], len(ir), 0, 0)
        if noiseComp == 1:  # indicates Lundeby's compensation
            t = np.zeros(len(irFilt))
            C = np.zeros(len(irFilt))
            sch = np.zeros_like(irFilt)
            for i in range(len(irFilt)):
                try:
                    t[i], C[i] = lundeby(irFilt[i], fs, 0.01)  # Ts = 10 ms
                except:
                    print("Error detected while analyzing " + str(int(centerFrequency_Hz[
                                                                          i])) + " Hz octave or 1/3 octave band. Results will omit EDT, T20 and T30 in this frequency band")
                sch[i] = schroeder(irFilt[i], t[i], C[i], 0)
        if noiseComp == 2:  # indicates Chu's compensation
            rms = np.zeros(len(irFilt))
            sch = np.zeros_like(irFilt)
            for i in range(len(irFilt)):
                rms[i] = chuCompensation(irFilt[i])
                sch[i] = schroeder(irFilt[i], len(irFilt[i]), 0, rms[i])
        ir_smooth = sch  # Smoothed response stored in ir_smooth variable
        ir_smooth_db = 10 * np.log10(np.abs(sch) + sys.float_info.epsilon)  # Smoothed response in dB
    if smoothing == 1:
        ir_smooth = medianf(irFilt, medianwindow)
        ir_smooth_db = 10 * np.log10(np.abs(ir_smooth) + sys.float_info.epsilon)

    ir_db = 10 * np.log10(
        np.abs(irFilt) + sys.float_info.epsilon)  # Un-smoothed response in dB (for comparison plot)

    m_edt = np.zeros(len(ir_smooth))  # Init. variables for room parameters.
    m_t20 = np.zeros(len(ir_smooth))
    m_t30 = np.zeros(len(ir_smooth))
    C50 = np.zeros(len(ir_smooth))
    C80 = np.zeros(len(ir_smooth))
    Ts = np.zeros(len(ir_smooth))
    for i in range(len(ir_smooth)):
        m_edt[i], m_t20[i], m_t30[i] = TR(ir_smooth_db[i], fs)  # EDT, T20 and T30 calculations
        C50[i], C80[i], Ts[i] = cParameters(ir_smooth[i], fs)  # C50, C80 and Ts calculations
    if IACC:  # if statement evaluates to TRUE if *args IACC parameter is passed to function.
        return ir_smooth_db, ir_db, m_edt, m_t20, m_t30, C50, C80, Tt, Ts, ir_IACC, EDTt
    else:
        return ir_smooth_db, ir_db, m_edt, m_t20, m_t30, C50, C80, Tt, Ts, EDTt


def calculateMain(ir, fs, analysis, smoothing, noiseComp, medianwindow, rangef, *IACC):
    """calculateMain function will be called by GUI. It calls calculateMono for every channel input in "ir" and
    calculates IACC parameters in the case of *args IACC argument is passed """

    if IACC:  # If IACC optional argument is passed, Stereo IR input is expected
        ir = np.transpose(ir)

        ir_smooth_dbL, ir_dbL, m_edtL, m_t20L, m_t30L, C50L, C80L, TtL, TsL, ir_IACCL, EDTtL = calculateMono(ir[0], fs,
                                                                                                             analysis,
                                                                                                             smoothing,
                                                                                                             noiseComp,
                                                                                                             medianwindow,rangef,
                                                                                                             IACC)
        ir_smooth_dbR, ir_dbR, m_edtR, m_t20R, m_t30R, C50R, C80R, TtR, TsR, ir_IACCR, EDTtR = calculateMono(ir[1], fs,
                                                                                                             analysis,
                                                                                                             smoothing,
                                                                                                             noiseComp,
                                                                                                             medianwindow,rangef,
                                                                                                             IACC)

        IACCearly = np.zeros(len(ir_IACCL))  # Init. IACC variables
        IACClate = np.zeros(len(ir_IACCL))
        IACCall = np.zeros(len(ir_IACCL))
        for i in range(len(ir_IACCL)):  # IACC calculation
            IACCearly[i], IACClate[i], IACCall[i] = IACCf(ir_IACCL[i], ir_IACCR[i], fs)

        if IACC[0] == 0:  # IACCearly, late or all chosen.
            varIACC = IACCearly
        if IACC[0] == 1:
            varIACC = IACClate
        if IACC[0] == 2:
            varIACC = IACCall

        return ir_smooth_dbL, ir_dbL, m_edtL, m_t20L, m_t30L, C50L, C80L, TtL, TsL, EDTtL, ir_smooth_dbR, ir_dbR, m_edtR, m_t20R, m_t30R, C50R, C80R, TtR, TsR, EDTtR, varIACC
    else:  # Mono IR input
        ir_smooth_db, ir_db, m_edt, m_t20, m_t30, C50, C80, Tt, Ts, EDTt = calculateMono(ir, fs, analysis, smoothing,
                                                                                         noiseComp,
                                                                                         medianwindow,rangef)
        return ir_smooth_db, ir_db, m_edt, m_t20, m_t30, C50, C80, Tt, Ts, EDTt
