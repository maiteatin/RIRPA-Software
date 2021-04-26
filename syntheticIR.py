import numpy as np
import soundfile as sf

fs = 48000
t = np.arange(0, 3, 1/fs)

A = 1
b = 3
M = 0.0005

y = A*np.e**(-b*t)
n = np.random.normal(0, 0.01, y.shape)
z = y*n
y = y*n + M*n

y = y/np.max(y)

TR = 3/(b*np.log10(np.e))
print(TR)
tc = -(np.log(M/A))/b
print(tc)

name = 'TR' + str(np.round(TR, 2)) + 's_tc' + str(np.round(tc, 2)) + 's'


sf.write('RIRs sintéticas/' + name + '.wav', y, fs)

# import matplotlib.pyplot as plt
# plt.plot(t,20*np.log10(y))
# # plt.plot(t,20*np.log10(z))
# # plt.plot(t,20*np.log10(M*n))
# plt.vlines(tc, -200, 0, colors='r')
# plt.show()
