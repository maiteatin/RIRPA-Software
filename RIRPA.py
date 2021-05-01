from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from Functions.filtroInverso import iss
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
from scipy import signal
import numpy as np
from Functions.audioRead import audioRead
from Functions.calculateMain import calculateMain
import csv
import os
import soundfile as sf

# GUI Main Window
root = Tk()  # This is the section of code which creates the main window
root.geometry('650x450')  # Window dimensions
root.configure(background='#FFFFFF')  # Background Color
root.title('Room Impulse Response Processor')  # Window title
# root.iconbitmap('images/icon.ico')
root.resizable(False, False)  # Non-resizable


# FUNCTIONS


def loadFunction():
    global rangef
    rangef=[]
    limitBands.set(0)
    global filename  # filename is path of the loaded IR and is used when calculateMain is called
    filename = filedialog.askopenfilename(
        title='Select an Impulse Response File', filetypes=[("WAV Files", "*.wav")])
    data, samplerate, path, duration, frames, channels = audioRead(filename)
    short_filename = os.path.basename(filename)
    statusLabel.configure(text='Load successful')  # Change status label
    for i in IR_tree.get_children():  # Clear existing data in IR_tree
        IR_tree.delete(i)
    IR_tree.insert(parent='', index='end', iid=1, text="",
                   values=(short_filename, round(duration, 2), samplerate, channels))  # Replace with new data
    if channels == 1:
        IACCLabel.config(fg='#cccccc')
        IACCOpt.config(state='disabled')
    if channels == 2:
        IACCLabel.config(fg='#000000')
        IACCOpt.config(state='active')
    button_calculate.config(state='active')
    return data, samplerate, path, duration, frames, channels


def helpFunction():
    # Toplevel object which will
    # be treated as a new window
    helpWindow = Toplevel(root)

    # Sets the title of the Toplevel widget
    helpWindow.title("Help")
    helpWindow.resizable(False, False) 
    # sets the geometry of toplevel
    helpWindow.geometry("500x650")

    # A Label widget to show in toplevel
    Label(helpWindow, text=open('help.txt', 'r', encoding="utf8").read(), wraplength=420, justify="left").pack()


def smoothingModeFunction():
    if smoothingVariable.get() == 0:  # Schroeder
        MMFWindowLabel.config(fg='#cccccc')  # Make Window Label Text Gray (Disabled)
        noiseCompLabel.config(fg='#000000')  # Make Noise Comp Label Text Black (Active)
        noiseOptMenu.config(state='active')
    if smoothingVariable.get() == 1:  # Moving Median Filter
        MMFWindowLabel.config(fg='#000000')  # Make Label Text Black (Active)
        noiseCompLabel.config(fg='#cccccc')  # Make Noise Comp Label Text Gray (Disabled)
        noiseOptMenu.config(state='disabled')


def openSweep():
    # GUI Main Window
    sweepWindow = Tk()  # This is the section of code which creates the main window
    sweepWindow.geometry('400x450')  # Window dimensions
    sweepWindow.configure(background='#FFFFFF')  # Background Color
    sweepWindow.title('Sine Sweep')  # Window title
    # root.iconbitmap('images/icon.ico')
    sweepWindow.resizable(False, False)  # Non-resizable

    # FUNCTIONS

    def helpFunction():
        # Toplevel object which will
        # be treated as a new window
        helpWindow = Toplevel(root)

        # Sets the title of the Toplevel widget
        helpWindow.title("Help")
        helpWindow.resizable(False, False)
        # sets the geometry of toplevel
        helpWindow.geometry("300x400")

        # A Label widget to show in toplevel
        Label(helpWindow,
              text=open('sweepHelp.txt', 'r').read(), wraplength=250, justify="left").pack()

    def generateFunction():

        global irSweep, sweepIRfilename
        try:
            sweepIRfilename = 'IR_' + os.path.basename(sweepPath)
        except:
            messagebox.showwarning('Error', 'Please specify a valid pathname.')
            raise ValueError('Please specify a valid pathname.')
        try:
            f1 = np.float64(sweepStart.get())
            f2 = np.float64(sweepEnd.get())
            d = np.float64(duration.get())
            if f1 <= 0 or f2 <= 0 or d <= 0 or f1 > f2:
                raise ValueError('Invalid o empty values')
        except:
            messagebox.showwarning('Error', 'Please specify valid start and end frequencies [Hz], and duration [s].')
            raise ValueError('Invalid o empty values')
        fs = np.float64(sampleFreq.get())
        sweepType = typeVariable.get()
        channels = channelVariable.get()
        irSweep = iss(channels, sweepData, f1, f2, d, fs, sweepType)  # Revisar formato de sweepData cuando es stereo

        for i in IR_tree.get_children():
            IR_tree.delete(i)

        IR_tree.insert(parent='', index='end', iid=1, text='',
                       values=(sweepIRfilename, np.round(sweepDuration, 2), fs, channels))
        sweepWindow.destroy()
        button_calculate.config(state='active')

        if channels == 1:
            IACCLabel.config(fg='#cccccc')
            IACCOpt.config(state='disabled')
        if channels == 2:
            IACCLabel.config(fg='#000000')
            IACCOpt.config(state='active')

    def saveFunction(y, fs, channels, filename):
        newfilename = filedialog.asksaveasfilename(initialdir="/", initialfile=filename, title="Save As",
                                                   filetypes=(("Audio File", "*.wav"), ("All Files", "*.*")),
                                                   defaultextension=".wav")
        fs = int(fs)
        sf.write(newfilename, y, fs)

    def generateIRfromSweepandIF(sweepData, IFData):
        global irSweep, sweepIRfilename
        irSweep = signal.fftconvolve(sweepData, IFData)  # Generate IR by convolving sweep and its inverse filter
        sweepIRfilename = 'IR_' + os.path.basename(sweepPath)
        for i in IR_tree.get_children():
            IR_tree.delete(i)

        IR_tree.insert(parent='', index='end', iid=1, text='',
                       values=(sweepIRfilename, np.round(sweepDuration, 2), sweepfs, sweepChannels))
        sweepWindow.destroy()
        button_calculate.config(state='active')

    def loadSweepFunction():
        global sweepData, sweepfs, sweepPath, sweepDuration, sweepChannels
        global IFData, IFfs, IFPath, IFDuration, IFChannels
        sweepFilename = filedialog.askopenfilename(
            title='Select a Sine Sweep File', filetypes=[("WAV Files", "*.wav")])
        sweepData, sweepfs, sweepPath, sweepDuration, sweepFrames, sweepChannels = audioRead(sweepFilename)
        if messagebox.askyesno("", "Would you like to load an inverse filter file too?"):
            inverseFilterFilename = filedialog.askopenfilename(title='Select an Inverse Filter File',
                                                               filetypes=[("WAV Files", "*.wav")])
            IFData, IFfs, IFPath, IFDuration, IFFrames, IFChannels = audioRead(inverseFilterFilename)
            messagestring = 'Successfully loaded files. \n Sweep: ' + os.path.basename(
                os.path.normpath(sweepFilename)) + '\n Inverse Filter: ' + os.path.basename(
                os.path.normpath(inverseFilterFilename)) + '\n Click OK to generate IR.'
            messagebox.showinfo("", messagestring)
            generateIRfromSweepandIF(sweepData, IFData)
        else:
            messagestring = 'Successfully loaded sweep file: ' + os.path.basename(
                os.path.normpath(sweepFilename)) + '\n Specify start and end frequencies, duration and type.'
            messagebox.showinfo("", messagestring)
            # Insert sweep data on entries
            duration.delete(0, END)
            # duration.insert(0, dur)
            # duration.config(state='disabled')
            sampleFreq.delete(0, END)
            sampleFreq.insert(0, sweepfs)
            sampleFreq.config(state='disabled')
            channelVariable.set(sweepChannels)
            channelOpt.config(state='disabled')
            statusLabelText(messagestring)  # Change status label
            sweepWindow.lift()

    def statusLabelText(string):
        # Modifies status label to whatever text is specified in string.
        statusLabel.configure(text=string)

    # Rectangle
    canvas = Canvas(sweepWindow, width=400, height=400)
    canvas.place(x=0, y=0)
    rectangle = canvas.create_rectangle(10, 22, 380, 330)

    # Buttons
    button_help = Button(sweepWindow, text='Help', command=helpFunction, padx=10)
    button_help.place(x=25, y=350)
    button_cancel = Button(sweepWindow, text='Cancel', command=sweepWindow.destroy, padx=10)  # Closes window
    button_cancel.place(x=200, y=350)
    button_generate = Button(sweepWindow, text='Generate IR', command=generateFunction, padx=10)
    button_generate.place(x=280, y=350)
    button_load = Button(sweepWindow, text='Load Sweep', command=loadSweepFunction, padx=10)
    button_load.place(x=25, y=42)

    # Labels

    sweepLabel = Label(sweepWindow, text='Inverse Filter Generator', font='Helvetica 18 bold').place(x=15, y=10)
    fromLabel = Label(sweepWindow, text='From').place(x=25, y=75)
    toLabel = Label(sweepWindow, text='To').place(x=40, y=105)
    durationLabel = Label(sweepWindow, text='Duration').place(x=25, y=160)
    # amplitudeLabel = Label(sweepWindow, text='Amplitude').place(x=25, y=190)
    channelsLabel = Label(sweepWindow, text='Channels').place(x=25, y=210)
    samplingRateLabel = Label(sweepWindow, text='Sampling Rate').place(x=25, y=250)
    typeLabel = Label(sweepWindow, text='Type').place(x=25, y=290)
    hzLabel1 = Label(sweepWindow, text='Hz').place(x=265, y=75)
    hzLabel2 = Label(sweepWindow, text='Hz').place(x=265, y=105)
    secondsLabel = Label(sweepWindow, text='s').place(x=295, y=160)
    # amplitudeLabel2 = Label(sweepWindow, text='(0-1.0)').place(x=295, y=190)
    hzLabel3 = Label(sweepWindow, text='Hz').place(x=320, y=250)

    # Entries
    sweepStart = Entry(sweepWindow)
    sweepStart.place(x=70, y=73)
    sweepEnd = Entry(sweepWindow)
    sweepEnd.place(x=70, y=103)
    duration = Entry(sweepWindow)
    duration.place(x=100, y=155)
    # amplitude = Entry(sweepWindow)
    # amplitude.place(x=100, y=185)
    sampleFreq = Entry(sweepWindow)
    sampleFreq.place(x=125, y=245)

    # Channels Option Menu
    channelOptionList = [1, 2]
    channelVariable = IntVar(sweepWindow)
    channelVariable.set(channelOptionList[0])

    channelOpt = OptionMenu(sweepWindow, channelVariable, *channelOptionList)
    channelOpt.config(width=2, font=('Helvetica', 12))
    channelOpt.place(x=100, y=210)

    # Sweep Type Radiobuttons

    typeVariable = IntVar(sweepWindow)
    typeVariable.set(0)  # Sets Linear Sweep as default

    R1 = Radiobutton(sweepWindow, text="Linear", variable=typeVariable, value=0)
    R1.place(x=90, y=290)
    R2 = Radiobutton(sweepWindow, text="Log", variable=typeVariable, value=1)
    R2.place(x=180, y=290)

    # Status Label
    statusLabel = Label(sweepWindow, text='Status: ready')
    statusLabel.pack(side=BOTTOM)

    # FILENAME
    filenameLabel = Label(sweepWindow, text='')
    filenameLabel.pack(side=BOTTOM)

    sweepWindow.mainloop()  # Main Loop of the program


def tree_insert(tree, values, parameters):
    # Delete existing information
    for i in tree.get_children():
        tree.delete(i)
    # Add new information
    j = 0
    for i in parameters:
        j = j + 1
        tree.insert(parent='', index='end', iid=j, text=i, values=values[j - 1])


def channelSelect(event):
    selected = int(CH_tree.focus())
    tree_insert(param_tree, values[selected - 1], parameters)
    updatePlot(-1)


def getParameters(ir, fs, channels, analysis, smoothing, noiseComp, MMFWindowLength, rangef, IACC):
    # Calculate all parameters from main function
    if MMFWindowLength / fs > len(ir) / (2 * fs):
        messagebox.showwarning("Error", "Please enter a shorter window length")
        raise ValueError('Please enter a shorter window length')
    if channels == 1:  # Mono
        ir_smooth_db, ir_db, EDT, T20, T30, C50, C80, Tt, Ts, EDTt = calculateMain(ir, fs, analysis, smoothing,
                                                                                   noiseComp,
                                                                                   MMFWindowLength,rangef)
        # Rounding to 3 decimal digits and convert to tuple for display in treeview
        C50 = tuple(np.round(C50, 3))
        C80 = tuple(np.round(C80, 3))
        T20 = tuple(np.round(T20, 3))
        T30 = tuple(np.round(T30, 3))
        EDT = tuple(np.round(EDT, 3))
        Ts = tuple(np.round(Ts, 3))
        EDTt = tuple(np.round(EDTt, 3))
        Tt = tuple(np.round(Tt, 3))

        # Replace spurious results
        for i in range(len(EDT)):
            if EDT[i] < 0.0 or np.isnan(EDT[i]) or EDT[i] > 15:
                y = list(EDT)
                y[i] = "-"
                EDT = tuple(y)
            if T20[i] < 0.0 or np.isnan(T20[i]) or T20[i] > 15:
                y = list(T20)
                y[i] = "-"
                T20 = tuple(y)
            if T30[i] < 0.0 or np.isnan(T30[i]) or T30[i] > 15:
                y = list(T30)
                y[i] = "-"
                T30 = tuple(y)
            if np.isnan(C50[i]):
                y = list(C50)
                y[i] = "-"
                C50 = tuple(y)
            if np.isnan(C80[i]):
                y = list(C80)
                y[i] = "-"
                C80 = tuple(y)
            if Ts[i] > len(ir) / fs or np.isnan(Ts[i]):
                y = list(Ts)
                y[i] = "-"
                Ts = tuple(y)
            if Tt[i] > len(ir) / fs:
                y = list(Tt)
                y[i] = "-"
                Tt = tuple(y)
            if EDTt[i] < 0.0 or np.isnan(EDTt[i]):
                y = list(EDTt)
                y[i] = "-"
                EDTt = tuple(y)

        values = (C50, C80, T20, T30, EDT, EDTt, Tt, Ts)
        parameters = ['C50 [dB]', 'C80[dB]', 'T20 [s]', 'T30 [s]', 'EDT [s]', 'EDTt [s]', 'Tt [s]', 'Ts [s]']
        irs = [ir_db, ir_smooth_db]
    if channels == 2:  # Stereo
        ir_smooth_dbL, ir_dbL, EDTL, T20L, T30L, C50L, C80L, TtL, TsL, EDTtL, ir_smooth_dbR, ir_dbR, EDTR, T20R, T30R, C50R, C80R, TtR, TsR, EDTtR, varIACC = calculateMain(
            ir, fs, analysis, smoothing, noiseComp, MMFWindowLength,centerFrequency_Hz, IACC)

        # Rounding to 3 decimal digits and convert to tuple for display in treeview
        C50L = tuple(np.round(C50L, 3))
        C50R = tuple(np.round(C50R, 3))
        C80L = tuple(np.round(C80L, 3))
        C80R = tuple(np.round(C80R, 3))
        T20L = tuple(np.round(T20L, 3))
        T20R = tuple(np.round(T20R, 3))
        T30L = tuple(np.round(T30L, 3))
        T30R = tuple(np.round(T30R, 3))
        EDTL = tuple(np.round(EDTL, 3))
        EDTR = tuple(np.round(EDTR, 3))
        TtL = tuple(np.round(TtL, 3))
        TtR = tuple(np.round(TtR, 3))
        TsL = tuple(np.round(TsL, 3))
        TsR = tuple(np.round(TsR, 3))
        EDTtL = tuple(np.round(EDTtL, 3))
        EDTtR = tuple(np.round(EDTtR, 3))
        varIACC = tuple(np.round(varIACC, 3))

        # Replace spurious results
        for i in range(len(EDTL)):
            if EDTL[i] < 0.0 or np.isnan(EDTL[i]) or EDTL[i] > 15:
                y = list(EDTL)
                y[i] = "-"
                EDTL = tuple(y)
            if T20L[i] < 0.0 or np.isnan(T20L[i]) or T20L[i] > 15:
                y = list(T20L)
                y[i] = "-"
                T20L = tuple(y)
            if T30L[i] < 0.0 or np.isnan(T30L[i]) or T30L[i] > 15:
                y = list(T30L)
                y[i] = "-"
                T30L = tuple(y)
            if np.isnan(C50L[i]):
                y = list(C50L)
                y[i] = "-"
                C50L = tuple(y)
            if np.isnan(C80L[i]):
                y = list(C80L)
                y[i] = "-"
                C80L = tuple(y)
            if TsL[i] > len(ir) / fs or np.isnan(TsL[i]):
                y = list(TsL)
                y[i] = "-"
                TsL = tuple(y)
            if TtL[i] > len(ir) / fs:
                y = list(TtL)
                y[i] = "-"
                TtL = tuple(y)
            if EDTtL[i] < 0.0 or np.isnan(EDTtL[i]):
                y = list(EDTtL)
                y[i] = "-"
                EDTtL = tuple(y)
            if EDTR[i] < 0.0 or np.isnan(EDTR[i]) or EDTR[i] > 15:
                y = list(EDTR)
                y[i] = "-"
                EDTR = tuple(y)
            if T20R[i] < 0.0 or np.isnan(T20R[i]) or T20R[i] > 15:
                y = list(T20R)
                y[i] = "-"
                T20R = tuple(y)
            if T30R[i] < 0.0 or np.isnan(T30R[i]) or T30R[i] > 15:
                y = list(T30R)
                y[i] = "-"
                T30R = tuple(y)
            if np.isnan(C50R[i]):
                y = list(C50R)
                y[i] = "-"
                C50R = tuple(y)
            if np.isnan(C80R[i]):
                y = list(C80R)
                y[i] = "-"
                C80R = tuple(y)
            if TsR[i] > len(ir) / fs or np.isnan(TsR[i]):
                y = list(TsR)
                y[i] = "-"
                TsR = tuple(y)
            if TtR[i] > len(ir) / fs:
                y = list(TtR)
                y[i] = "-"
                TtR = tuple(y)
            if EDTtR[i] < 0.0 or np.isnan(EDTtR[i]):
                y = list(EDTtR)
                y[i] = "-"
                EDTtR = tuple(y)
            if varIACC[i] < -1 or varIACC[i] > 1.1:
                varIACC[i] = "-"
            elif varIACC[i] > 1:
                varIACC[i] = 1

        valuesL = (C50L, C80L, T20L, T30L, EDTL, EDTtL, TtL, TsL, varIACC)
        valuesR = (C50R, C80R, T20R, T30R, EDTR, EDTtR, TtR, TsR, varIACC)
        values = [valuesL, valuesR]
        IACC_strings = ['IACC Early', 'IACC Late', 'IACC All']
        IACC_string = IACC_strings[IACC]
        parameters = ['C50 [dB]', 'C80[dB]', 'T20 [s]', 'T30 [s]', 'EDT [s]', 'EDTt [s]', 'Tt [s]', 'Ts [s]',
                      IACC_string]
        irs = [ir_dbL, ir_smooth_dbL, ir_dbR, ir_smooth_dbR]
    return values, parameters, irs


def timeArray(y, fs):
    t = np.arange(0, len(y) / fs, 1 / fs)
    return t


def plotFormat(ax, label):
    ax.grid()
    if label == 'Global':
        ax.set_title(label)
    else:
        ax.set_title(label + 'Hz')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Level [dB]')
    ax.set_ylim([-100, 3])
    ax.legend()


def generateFigure(ir, decay, Tt, Ts):
    fig = Figure(figsize=(1, 1))
    ax = fig.add_subplot()
    t = timeArray(ir, fs)
    t = t[:len(ir)]
    ax.plot(t, ir, label='Impulse Response')
    if smoothingVariable.get() == 0:
        ax.plot(t, decay, label='Schroeder Decay')
    elif smoothingVariable.get() == 1:
        ax.plot(t, decay, label='Mov. Median Filter Decay ')
    if Tt != '-':
        ax.axvline(x=Tt, linewidth=0.5, color='r', linestyle='--', label='Tt')
    if Ts != '-':
        ax.axvline(x=Ts, linewidth=0.5, color='g', linestyle='--', label='Ts')
    plotFormat(ax, 'Global')
    return fig, ax


def updatePlot(j):  # j is the index of frequency band selected in table
    ch = int(CH_tree.focus())  # get value of selected channel in table (1 for L, 2 for R)
    if ch == 1:
        ir = irs[0][j]
        decay = irs[1][j]
    if ch == 2:
        ir = irs[2][j]
        decay = irs[3][j]
    Tt = values[0][6][j]
    Ts = values[0][7][j]
    ax.clear()  # Clear existing plot
    t = timeArray(ir, fs)
    t = t[:len(ir)]
    ax.plot(t, ir, label='Impulse Response')
    if smoothingVariable.get() == 0:
        ax.plot(t, decay, label='Schroeder Decay')
    elif smoothingVariable.get() == 1:
        ax.plot(t, decay, label='Mov. Median Filter Decay ')
    if Tt != '-':
        ax.axvline(x=Tt, linewidth=0.5, color='r', linestyle='--', label='Tt')
    if Ts != '-':
        ax.axvline(x=Ts, linewidth=0.5, color='g', linestyle='--', label='Ts')
    plotFormat(ax, centerFrequency_Hz[j])
    plotCanvas.draw()  # Update canvas


def updateProgressbar(x):
    progress.set(x)
    percent.set(str(x) + "%")
    root.update()


def calculateFunction():
    global fs  # To generate time array in plots
    ir_filename = IR_tree.item(1)['values'][0]  # Get filename from treeview
    if ir_filename != sweepIRfilename:  # When IR is loaded directly, get data from its path
        ir, fs, path, duration, frames, channels = audioRead(filename)
        short_filename = os.path.basename(filename)
    else:  # An IR has been generated from the Sine Sweep window and there is no need to read an audio file
        fs = sweepfs
        duration = sweepDuration
        channels = sweepChannels
        ir = irSweep
        short_filename = sweepIRfilename

    updateProgressbar(10)

    # Get GUI variable values
    analysis = analysisVariable.get()
    global smoothing
    smoothing = smoothingVariable.get()
    noiseComp = noiseCompOptionList.index(noiseCompVariable.get())
    if not MMFWindowEntry.get():  # If entry is empty
        MMFWindowLength = 1 / 20  # Default
    else:
        try:
            if np.float64(MMFWindowEntry.get()) / 1000 > 0 and np.float64(MMFWindowEntry.get()) / 1000 * fs > 2:
                MMFWindowLength = np.float64(MMFWindowEntry.get()) / 1000  # in seconds
            else:
                messagebox.showwarning("Error", "Please enter a valid window lenght in miliseconds")
        except:
            messagebox.showwarning("Error", "Please enter a valid window lenght in miliseconds")
    MMFWindowLength = int(MMFWindowLength * fs)  # in samples
    IACC = IACCOptionList.index(IACCVariable.get())

    updateProgressbar(20)

    # Generate new window
    global window
    window = Toplevel(root)
    window.title("Acoustic Parameters")
    window.resizable(False, False)
    window.geometry("1200x700")
    window.withdraw()  # Hide window until function is complete

    global centerFrequency_Hz
    # Table
    if analysis == 1:  # One Third Octave Bands
        centerFrequency_Hz = ['25', '31.5', '40', '50', '63', '80', '100', '125', '160', '200', '250', '315',
                              '400', '500', '630', '800', '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k',
                              '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k', "Global"]
    if analysis == 0:  # Octave Bands
        centerFrequency_Hz = ['31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k', "Global"]

    if limitBands.get() == 1:
        newRange.append("Global")
        centerFrequency_Hz = newRange

    param_frame = Frame(window, width=1000, height=100)
    global param_tree  # Revisar esto, tuve que ponerlo para que anduviese la funcion channelSelect
    param_tree = ttk.Treeview(param_frame, height=5)
    param_tree['columns'] = centerFrequency_Hz
    param_tree.column("#0", width=80, stretch=False)
    for i in range(len(centerFrequency_Hz)):
        param_tree.column(centerFrequency_Hz[i], width=60, anchor='e')
        param_tree.heading(centerFrequency_Hz[i], text=centerFrequency_Hz[i], command=lambda j=i: updatePlot(j))

    # Horizontal Scrollbar
    param_scrollbar = Scrollbar(param_frame, orient=HORIZONTAL)
    param_scrollbar.configure(command=param_tree.xview)
    param_tree.configure(xscrollcommand=param_scrollbar.set)
    param_frame.pack_propagate(0)
    param_scrollbar.pack(side="bottom", fill="x")
    param_tree.pack(side="top", fill="both", expand=True)

    # Buttons frame
    buttons_frame = Frame(window, width=200, height=300)
    # Back to setup button
    button_back = Button(buttons_frame, text='Back to setup...', command=lambda: window.destroy(), padx=10)
    button_back.place(relx=0.5, rely=0.2, anchor=CENTER)
    # Save button
    button_CSV = Button(buttons_frame, text='Export results to CSV...', command=lambda: exportCSVFunction(param_tree),
                        padx=10)
    button_CSV.place(relx=0.5, rely=0.3, anchor=CENTER)
    # Help button
    button_help2 = Button(buttons_frame, text='Help', command=lambda: helpFunction(), padx=10)
    button_help2.place(relx=0.5, rely=0.4, anchor=CENTER)

    # Channels table
    global CH_tree  # Revisar esto, tuve que ponerlo para que me anduviese la funcion channelSelect
    CH_tree = ttk.Treeview(buttons_frame, height=2)
    CH_tree.column("#0", width=0, stretch=False)
    CH_tree.heading("#0", text="", anchor=W)
    CH_tree['columns'] = "Channel"
    CH_tree.column("Channel", width=320, stretch=False)
    CH_tree.heading("Channel", text="Channel", anchor=W)
    if channels == 1:
        CH_tree.insert(parent='', index='end', iid=1, text='', values=short_filename)
    if channels == 2:
        CH_tree.insert(parent='', index='end', iid=1, text='', values=short_filename + '[L]')
        CH_tree.insert(parent='', index='end', iid=2, text='', values=short_filename + '[R]')
    CH_tree.focus_set()  # Set 1st channel as default selected row
    CH_tree.selection_set((1, 1))  # Set 1st channel as default selected row
    CH_tree.focus(1)  # Set 1st channel as default selected row
    CH_tree.place(relx=0.5, rely=0.7, anchor=CENTER)
    CH_tree.bind("<ButtonRelease-1>", channelSelect)

    updateProgressbar(50)

    global values, parameters, irs
    values, parameters, irs = getParameters(ir, fs, channels, analysis, smoothing, noiseComp, MMFWindowLength, rangef,IACC)
    if channels == 2:
        tree_insert(param_tree, values[0],
                    parameters)  # Insert values into table using tree_insert function (L channel by default)
    else:
        tree_insert(param_tree, values, parameters)  # Insert values into table using tree_insert function
        values = [values]  # This is to ensure compatibility with  channelSelect function

    updateProgressbar(80)

    # CANVAS AND PLOT
    global plotCanvas, fig, ax
    Tt_G = values[0][6][-1]
    Ts_G = values[0][7][-1]
    fig, ax = generateFigure(irs[0][-1],
                             irs[1][-1], Tt_G,
                             Ts_G)  # As default, plot Left channel (if stereo), 1 kHz band.
    plotCanvas = FigureCanvasTkAgg(fig, master=window)
    plotCanvas.draw()

    updateProgressbar(90)

    # Setting positions by grid
    plotCanvas.get_tk_widget().grid(row=0, column=1, sticky=NSEW)
    buttons_frame.grid(row=0, column=2, sticky=NSEW)
    param_frame.grid(row=1, column=1, columnspan=2, sticky=NSEW)
    window.grid_columnconfigure(1, weight=10)
    window.grid_columnconfigure(2, weight=2)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.deiconify()  # Show window

    limitBands.set(0) # Reset frequency bands range limiter to full band
    updateProgressbar(100)


def exportCSVFunction(param_tree):
    CSVfilename = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", defaultextension=".csv",
                                               filetypes=(("CSV File,", "*.csv"), ("All Files", "*")))
    with open(CSVfilename, mode='w') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')
        firstrow = [''] + list(param_tree['columns'])
        exp_writer.writerow(firstrow)  # Writes Frequency Band Values
        for row_id in param_tree.get_children():
            row = [param_tree.item(row_id)['text']] + param_tree.item(row_id)['values']  # Writes Parameter Values
            exp_writer.writerow(row)


def rangeSelect():
    # GUI Main Window
    rangeWindow = Tk()  # This is the section of code which creates the main window
    rangeWindow.geometry('350x200')  # Window dimensions
    rangeWindow.configure(background='#FFFFFF')  # Background Color
    rangeWindow.title('Analyzed Frequency Range')  # Window title
    # root.iconbitmap('images/icon.ico')
    rangeWindow.resizable(False, False)  # Non-resizable
    global centerFrequency_Hz
    if analysisVariable.get() == 0:
        centerFrequency_Hz = ['31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k']
    else:
        centerFrequency_Hz = ['25', '31.5', '40', '50', '63', '80', '100', '125', '160', '200', '250', '315',
                              '400', '500', '630', '800', '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k',
                              '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k']

    rangeMinOptionList = centerFrequency_Hz
    rangeMinVariable = StringVar(rangeWindow)
    rangeMinVariable.set(rangeMinOptionList[0])
    rangeMinOptMenu = OptionMenu(rangeWindow, rangeMinVariable, *rangeMinOptionList)
    rangeMinOptMenu.config(width=13, font=('Helvetica', 12))
    rangeMinOptMenu.place(x=25, y=75)
    fMin = rangeMinOptionList.index(rangeMinVariable.get())

    rangeMaxOptionList = centerFrequency_Hz
    rangeMaxVariable = StringVar(rangeWindow)
    rangeMaxVariable.set(rangeMaxOptionList[-1])
    rangeMaxOptMenu = OptionMenu(rangeWindow, rangeMaxVariable, *rangeMaxOptionList)
    rangeMaxOptMenu.config(width=13, font=('Helvetica', 12))
    rangeMaxOptMenu.place(x=200, y=75)
    fMax = rangeMaxOptionList.index(rangeMaxVariable.get())

    fromLabel = Label(rangeWindow, text='From')
    fromLabel.place(x=25, y=50)
    toLabel = Label(rangeWindow, text='To')
    toLabel.place(x=200, y=50)


    def rangeOkFunction(centerFrequency_Hz):
        fMin = rangeMinOptionList.index(rangeMinVariable.get())
        fMax = rangeMaxOptionList.index(rangeMaxVariable.get())
        global rangef
        rangef = [fMin,fMax]
        global newRange
        newRange = centerFrequency_Hz[fMin:fMax+1]
        if centerFrequency_Hz == []:
            messagebox.showwarning("Error", "Please select a valid interval")
        limitBands.set(1) # Indicates that bands to be calculated and displayed have been limited
        rangeWindow.destroy()

    rangeOk = Button(rangeWindow, text='Confirm', command=lambda: rangeOkFunction(centerFrequency_Hz), padx=10).place(x=130, y=120)

# MAIN WINDOW LAYOUT
# Rectangle
canvas = Canvas(root, width=800, height=1000)
canvas.place(x=0, y=0)
rectangle1 = canvas.create_rectangle(10, 48, 640, 130)
rectangle2 = canvas.create_rectangle(10, 160, 400, 230)
rectangle3 = canvas.create_rectangle(10, 260, 400, 320)
rectangle4 = canvas.create_rectangle(10, 350, 400, 410)
rectangle5 = canvas.create_rectangle(420, 160, 640, 230)
rectangle6 = canvas.create_rectangle(420, 260, 640, 320)

# Buttons
button_help = Button(root, text='Help', command=helpFunction, padx=10).place(x=520, y=10)
button_close = Button(root, text='Close', command=root.quit, padx=10).place(x=580, y=10)  # Closes window
button_load = Button(root, text='Load IR...', command=loadFunction, padx=10).place(x=5, y=10)
button_sweep = Button(root, text='Load Sine Sweep...', command=openSweep, padx=10).place(x=90, y=10)
global button_calculate
button_calculate = Button(root, text='Calculate', command=calculateFunction, state='disabled', padx=60, pady=20)
button_calculate.place(x=435, y=350)

# PROGRESS BAR
percent = StringVar()
progress = DoubleVar()
percentLabel = Label(root, textvariable=percent).place(x=600, y=410)
# s = ttk.Style()
# s.theme_use('default')
# s.configure("bar.Horizontal.TProgressbar", throughcolor='red')
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=160, variable=progress, mode='determinate')
progress_bar.place(x=436, y=415)

# progress_bar.lower()  # Hide
# pb_window.withdraw()  # Hide window upon GUI launch


# Labels
IRLabel = Label(root, text='Impulse Response', font='Helvetica 18 bold').place(x=15, y=35)
analysisLabel = Label(root, text='Analysis', font='Helvetica 18 bold').place(x=15, y=150)
smoothingLabel = Label(root, text='Smoothing', font='Helvetica 18 bold').place(x=15, y=245)
noiseCompLabel = Label(root, text='Background Noise Compensation', font='Helvetica 18 bold')
noiseCompLabel.place(x=15, y=335)
IACCLabel = Label(root, text='IACC Integration', font='Helvetica 18 bold', fg='#cccccc')
IACCLabel.place(x=430, y=150)
MMFWindowLabel = Label(root, text='Window Length', font='Helvetica 18 bold', fg='#cccccc')
MMFWindowLabel.place(x=430, y=250)

# Entries
MMFWindowEntry = Entry(root)
MMFWindowEntry.place(x=430, y=280, width=80)
MMFWindowLabel2 = Label(root, text='[ms] (optional)').place(x=510, y=282)

# Noise Compensation Option Menu (Lundeby, Chu, No compensation)
noiseCompOptionList = ["No compensation", "Lundeby", "Chu"]
noiseCompVariable = StringVar(root)
noiseCompVariable.set(noiseCompOptionList[0])  # Sets No Compensation as default

noiseOptMenu = OptionMenu(root, noiseCompVariable, *noiseCompOptionList)
noiseOptMenu.config(width=13, font=('Helvetica', 12))
noiseOptMenu.place(x=25, y=370)

# IACC Option Menu (Early, Late, All)
IACCOptionList = ["Early (0-80 ms)", "Late (80-inf ms)", "All (0-inf ms)"]
IACCVariable = StringVar(root)
IACCVariable.set(IACCOptionList[0])  # Sets Early as default

IACCOpt = OptionMenu(root, IACCVariable, *IACCOptionList)
IACCOpt.config(width=20, font=('Helvetica', 12))
IACCOpt.place(x=435, y=190)
IACCOpt.config(state='disabled')

# Analysis Radiobuttons
analysisVariable = IntVar(root)
analysisVariable.set(0)  # Sets Octave Bands as default

R1 = Radiobutton(root, text="Octave Bands", variable=analysisVariable, value=0)
R1.place(x=25, y=190)
R2 = Radiobutton(root, text="1/3 Octave Bands", variable=analysisVariable, value=1).place(x=140, y=190)
freqbutton = Button(root, text="Choose Range", padx=5, command=rangeSelect)
freqbutton.place(x=285, y=190)

# Smoothing Radiobuttons
smoothingVariable = IntVar(root)
rb_schroeder = Radiobutton(root, text="Schroeder", variable=smoothingVariable, value=0,
                           command=smoothingModeFunction).place(x=25, y=280)
rb_mmf = Radiobutton(root, text="Moving Median Filter", variable=smoothingVariable, value=1,
                     command=smoothingModeFunction).place(x=160, y=280)

# Impulse response information table
IR_tree = ttk.Treeview(root, height=1)
IR_tree['columns'] = ("Filename", "Duration", "Sample Frequency", "Channels")
IR_tree.column("#0", width=0, stretch=False)
IR_tree.column("Filename", anchor=W, width=200, minwidth=200, stretch=False)
IR_tree.column("Duration", anchor=W, width=100, minwidth=100, stretch=False)
IR_tree.column("Sample Frequency", anchor=W, width=150, minwidth=150, stretch=False)
IR_tree.column("Channels", anchor=W, width=150, minwidth=150, stretch=False)

IR_tree.heading("#0", text="", anchor=W)
IR_tree.heading("Filename", text="File", anchor=W)
IR_tree.heading("Duration", text="Duration [s]", anchor=W)
IR_tree.heading("Sample Frequency", text="Sample Frequency [Hz]", anchor=W)
IR_tree.heading("Channels", text="Channels", anchor=W)

# Variables
filename = ''
duration = ''
samplerate = ''
channels = ''
# data = ''
path = ''
frames = ''
sweepIRfilename = ''
rangef =[]

# Initialize IR tree values
IR_tree.insert(parent='', index='end', iid=0, text="", values=(filename, duration, samplerate, channels))
IR_tree.place(x=20, y=75)

# Status Label
statusLabel = Label(root, text='Status: ready')
statusLabel.pack(side=BOTTOM)
limitBands = IntVar(root)
limitBands.set(0)

root.mainloop()  # Main Loop of the program
