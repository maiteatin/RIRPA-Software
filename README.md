# RIRPA-Software

#### How to use RIRPA

RIRPA (which stands for Room Impulse Response Processing Application) is an open source software designed for processing measured impulse response files and obtaining their acoustic parameters.

Note: this application is only compatible with .wav audio files.

1) Select “Load IR…” or “Load Sine Sweep…”

2) If “Load Sine Sweep” is selected, a new window will open where a Sweep File can be loaded. Optionally, its corresponding Inverse Filter File can be loaded. Otherwise, the Sweep Data can be entered manually (Start and Stop Frequencies, Duration and Type). Click “Generate IR” to generate the Impulse Response. You will be returned to the Main Window where the generated IR’s information will be displayed on the table.

3) Select Analysis Mode, Smoothing Mode, Background Noise Compensation (if Schroeder is selected) or Window Length (if MMF is selected), and IACC Integration (only for binaural IRs).

4) Click Calculate.

5) The results are displayed on a new window (Acoustic Parameters). The information displayed on the table can be changed by selecting the Channel on the right hand side.  The plots can be updated by clicking on each frequency band’s header on the table.

6) Results can be saved as a .csv file by clicking on “Export results to CSV…”


RIRPA Software is developed entirely in Python with a `Python 3.8` base interpreter. Below are the libraries used and their version:

- `tk 0.1.0`
- `wave 0.0.2`
- `soundfile 0.10.3.post1`
- `numpy 1.20.2`
- `scipy 1.6.3`
- `matplotlib 3.4.1`


###### Developed by Joaquin Ponferrada (joacoponfe@gmail.com), Alejandro Sosa Welford (alejandrososawelford@gmail.com) and Maite Atín (maiteatin@gmail.com) for Acoustic Instruments and Measurements (UNTREF) 
###### April 2021
