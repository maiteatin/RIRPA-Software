from tkinter import *
from tkinter import filedialog
from filtroInverso import iss
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import soundfile as sf
import numpy as np
from audioRead import audioRead

# GUI Main Window
root = Tk()  # This is the section of code which creates the main window
root.geometry('400x420')  # Window dimensions
root.configure(background='#FFFFFF')  # Background Color
root.title('Sine Sweep')  # Window title
root.iconbitmap('images/icon.ico')
root.resizable(False, False)  # Non-resizable


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
    f1 = np.float64(sweepStart.get())
    f2 = np.float64(sweepEnd.get())
    d = np.float64(duration.get())
    fs = np.float64(sampleFreq.get())
    sweepType = typeVariable.get()
    channels = channelVariable.get()
    y, u = iss(f1, f2, d, fs, sweepType)

    # Generate Filename
    if sweepType == 0:
        f_type = 'LinearSineSweep'
    else:
        f_type = 'LogSineSweep'

    if channels == 1:
        f_channels = 'Mono'
    if channels == 2:
        f_channels = 'Stereo'
    # Strings
    f_duration = str(duration.get())+'s'
    f_fstart = str(sweepStart.get())+'Hz'
    f_fend = str(sweepEnd.get())+'Hz'
    f_fs = str(sampleFreq.get())+'Hz'
    f_amplitude = 'Amplitude:'+str(amplitude.get())
    filename = f_type+'_'+f_duration+'_'+f_fstart+'_'+f_fend+'_'+f_amplitude+'_'+f_fs+'_'+f_channels+'.wav'
    #filenameLabel.config(text=filename) # Update filename label
    # Create new window
    sweep_window = Toplevel(root)
    sweep_window.title(filename)
    sweep_window.resizable(False,False)
    sweep_window.geometry("600x400")
    fig = Figure(figsize=(5, 3), dpi=100)
    fig.add_subplot(111).plot(y)
    newcanvas = FigureCanvasTkAgg(fig, master=sweep_window)  # A tk.DrawingArea.
    newcanvas.draw()
    newcanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
    button_save = Button(sweep_window, text='Save As...', command= lambda: saveFunction(y, fs, channels, filename), padx=10)
    button_save.place(x=500, y=350)

def saveFunction(y, fs, channels, filename):
    newfilename = filedialog.asksaveasfilename(initialdir="/", initialfile=filename, title="Save As",
                                    filetypes=(("Audio File", "*.wav"), ("All Files", "*.*")),
                                    defaultextension=".wav")
    fs = int(fs)
    sf.write(newfilename, y, fs)

def loadSweepFunction():
    filename = filedialog.askopenfilename(
        title='Select a Sine Sweep File', filetypes=[("WAV Files", "*.wav")])

    # Read data from sweep file and insert it on entries
    data, samplerate, path, dur, frames, channels = audioRead(filename)
    duration.delete(0,END)
    duration.insert(0,dur)
    duration.config(state='disabled')
    sampleFreq.delete(0,END)
    sampleFreq.insert(0, samplerate)
    sampleFreq.config(state='disabled')
    channelVariable.set(channels)
    channelOpt.config(state='disabled')
    statusLabelText('Successfully loaded file. \n Verify that above information is correct and modify accordingly.')   # Change status label

def statusLabelText(string):
    # Modifies status label to whatever text is specified in string.
    statusLabel.configure(text=string)

def modeFunction():
    statusLabelText('')
    # Refresh all entries
    sweepStart.delete(0, END)
    sweepEnd.delete(0, END)
    amplitude.delete(0, END)
    duration.delete(0, END)
    sampleFreq.delete(0, END)
    if modeVariable.get() == 0:
        button_load.configure(state='active')
        button_generate.configure(text='Generate IR')
        button_cancel.place(x=200, y=350)
        button_generate.place(x=280, y=350)
    if modeVariable.get() == 1:
        button_load.configure(state='disabled')
        button_generate.configure(text='Generate Sine Sweep')
        button_cancel.place(x=140, y=350)
        button_generate.place(x=220, y=350)
        # Activate entries and lists: duration, fs, channels
        duration.config(state='normal')
        sampleFreq.config(state='normal')
        channelOpt.config(state='normal')


# Rectangle
canvas = Canvas(root, width=400, height=400)
canvas.place(x=0, y=0)
rectangle = canvas.create_rectangle(10, 22, 380, 330)

# Buttons
button_help = Button(root, text='Help', command=helpFunction, padx=10)
button_help.place(x=25, y=350)
button_cancel = Button(root, text='Cancel', command=root.quit, padx=10) # Closes window
button_cancel.place(x=200, y=350)
button_generate = Button(root, text='Generate IR', command=generateFunction, padx=10)
button_generate.place(x=280, y=350)
button_load = Button(root, text='Load Sweep', command=loadSweepFunction,padx=10)
button_load.place(x=260, y=42)

# Labels
sweepLabel = Label(root, text='Sweep', font='Helvetica 18 bold').place(x=15, y=10)
fromLabel = Label(root, text='From').place(x=25,y=75)
toLabel = Label(root, text='To').place(x=40, y=105)
durationLabel = Label(root, text='Duration').place(x=25,y=160)
amplitudeLabel = Label(root, text='Amplitude').place(x=25,y=190)
channelsLabel = Label(root, text='Channels').place(x=25,y=220)
samplingRateLabel = Label(root, text='Sampling Rate').place(x=25,y=250)
typeLabel = Label(root, text='Type').place(x=25, y=290)
hzLabel1 = Label(root, text='Hz').place(x=265, y=75)
hzLabel2 = Label(root, text='Hz').place(x=265, y=105)
secondsLabel = Label(root,text='s').place(x=295, y=160)
amplitudeLabel2 = Label(root,text='(0-1.0)').place(x=295, y=190)
hzLabel3 = Label(root, text='Hz').place(x=320, y=250)

# Entries
sweepStart = Entry(root)
sweepStart.place(x=70,y=73)
sweepEnd = Entry(root)
sweepEnd.place(x=70,y=103)
duration = Entry(root)
duration.place(x=100,y=155)
amplitude = Entry(root)
amplitude.place(x=100,y=185)
sampleFreq = Entry(root)
sampleFreq.place(x=125,y=245)

# Channels Option Menu
channelOptionList = [1, 2]
channelVariable = IntVar(root)
channelVariable.set(channelOptionList[0])

channelOpt = OptionMenu(root, channelVariable, *channelOptionList)
channelOpt.config(width=2, font=('Helvetica', 12))
channelOpt.place(x=100,y=220)


# Load or Generate Radiobuttons
modeVariable = IntVar(root)
modeVariable.set(0) # Sets Load as default mode

R_load = Radiobutton(root, text="Load", variable=modeVariable, value=0,command=modeFunction).place(x=25, y=45)
R_generate = Radiobutton(root, text="Generate", variable=modeVariable, value=1,command=modeFunction).place(x=100, y=45)

# Sweep Type Radiobuttons

typeVariable = IntVar(root)
typeVariable.set(0) # Sets Linear Sweep as default

R1 = Radiobutton(root, text="Linear", variable=typeVariable, value=0).place(x=90, y=290)
R2 = Radiobutton(root, text="Log", variable=typeVariable, value=1).place(x=180, y=290)

# Status Label
statusLabel = Label(root, text='Status: ready')
statusLabel.pack(side=BOTTOM)

# FILENAME
filenameLabel = Label(root, text='')
filenameLabel.pack(side=BOTTOM)

root.mainloop()  # Main Loop of the program
