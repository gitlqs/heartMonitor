# -*- coding: utf-8 -*-

import wave
import pywt
import numpy as np
import matplotlib.pyplot as plt

wf = wave.open('wav/filteredShort.wav')
data = wf.readframes(-1)
signal = np.fromstring(data, 'Int16')
signal = signal/np.max(signal)
signal = signal[::10]

coef, freqs=pywt.cwt(signal,np.arange(1,129),'gaus1')

fig = plt.figure()

ax1 = fig.add_subplot(2,1,2)
ax1.plot(np.arange(len(signal)), signal, linewidth=1)
#ax1.set_ylim([-50000,50000])

ax2 = fig.add_subplot(2,1,1)
ax2.matshow(coef)





plt.show()