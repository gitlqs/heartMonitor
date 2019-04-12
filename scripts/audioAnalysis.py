# -*- coding: utf-8 -*-

import wave
#import pyaudio
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib import style

#CHUNK = 8000

wf = wave.open('filtered.wav')

#instantiate PyAudio (1)
#p = pyaudio.PyAudio()

#open stream (2)
#stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#               channels=wf.getnchannels(),
#               rate=wf.getframerate(),
#               output=True)

# read data
# data = wf.readframes(CHUNK)
# data = data[4800:7800]

data = wf.readframes(-1)
data = np.fromstring(data, 'Int16')
#signal = signal[::10]

#filterWindowLength = 101
#filteredSignal = []
#for i in range(len(signal) - int(filterWindowLength/2)):
#    filteredSignal.append(np.average(signal[i:filterWindowLength+i]))


#x = np.arange(len(signal))

#style.use('fivethirtyeight')
#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)



#ax1.plot(x, signal, linewidth=1)
#ax1.set_ylim([-20000,20000])

#plt.plot(data, linewidth=1)

absData = np.abs(data)
normAbsData = absData/np.max(absData)

index = []
delaytime = 0;



for i in range(len(normAbsData)):
    if i<delaytime:
        continue
    if normAbsData[i] > 0.5:
        index.append(i)
        delaytime = i+3000
        
        
if len(index)-1 <= 0:
        print('Bad Signal Quality, Replace the Sensor.')  
else:
    averageDistance = (index[-1]-index[0])/(len(index)-1)
    heartrate = 60/(averageDistance/6000)  
    
    if heartrate > 150 or heartrate < 50:
        print('Bad Signal Quality, Replace the Sensor.')
    else:
        print("Heart Rate: {}".format(int(heartrate)) + ' BPM')


wf = wave.open('rawData.wav')
beforeFilter = wf.readframes(-1)
beforeFilter = np.fromstring(beforeFilter, 'Int16')

figure = plt.figure()
ax1 = figure.add_subplot(2,1,1)
ax2 = figure.add_subplot(2,1,2)

ax1.plot(beforeFilter, linewidth=1)
ax2.plot(data, linewidth=1)

#ax1.title(['Before Filter'])
#ax2.title('After Filter')

plt.show()

#plt.plot(data, linewidth=1)


