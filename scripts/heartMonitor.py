# -*- coding: utf-8 -*-

import pyaudio
#import wave

import numpy as np
import math

import matplotlib.pyplot as plt
from matplotlib import style

CUT_OFF_FREQ = 100.0

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 6000

FIRST_TRIAL = True



p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

#def animateCallBack(i):
#    row = np.array([float(i) for i in line])
#    if len(row) == 64:
#        row = np.log10(row)
#        pic.append(row)
#        if len(pic)>128:
#            pic.pop(0)
#        ax1.clear()
#        ax1.imshow(np.transpose(pic))
#        ax1.grid(False)

def running_mean(x, windowSize):
  cumsum = np.cumsum(np.insert(x, 0, 0)) 
  return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize


def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

    if sample_width == 1:
        dtype = np.uint8 # unsigned char
    elif sample_width == 2:
        dtype = np.int16 # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)

    return channels


while True:
    
    frames = []
    
    if FIRST_TRIAL:
        RECORD_SECONDS = 5
        first_trail = False
    else:
        RECORD_SECONDS = 5
        
#    print("* recording")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
#    print("* done recording")
    
    signal = np.fromstring(b''.join(frames), 'Int16')
    
    # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
    freqRatio = (CUT_OFF_FREQ/RATE)
    N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)

    # Use moviung average (only on first channel)
    filtered = running_mean(signal, N).astype(signal.dtype)
    
    absData = np.abs(filtered)
    normAbsData = absData/np.max(absData)
    
    
    delaytime = 0
    index = []
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
        if heartrate > 150 or heartrate < 40:
            print('Bad Signal Quality, Replace the Sensor.')
        else:
            print("Heart Rate: {}".format(int(heartrate)) + ' BPM')
    
