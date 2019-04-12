# -*- coding: utf-8 -*-

import pyaudio
#import struct
import numpy as np
import matplotlib.pyplot as plt
#import wave

from scipy.fftpack import fft
from scipy.ndimage.filters import gaussian_filter1d

plt.ion()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(
        format=FORMAT, 
        channels=CHANNELS, 
        rate=RATE, 
        input=True, 
        output=True,
        frames_per_buffer=CHUNK
)

multiplier = 20

fig = plt.figure()
fig.tight_layout()
ax1 = plt.subplot(3, 1, 1)
ax2 = plt.subplot(3, 1, 2)
ax3 = plt.subplot(3, 1, 3)

fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)

left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.5   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.2   # the amount of width reserved for blank space between subplots
hspace = 0.2   # the amount of height reserved for white space between subplots

x_buffer = np.arange(0, CHUNK*multiplier, 1)/RATE
line_buffer, = ax1.plot(x_buffer, np.random.rand(CHUNK*multiplier), 'r')
ax1.set_ylim(-20000,20000)
#ax1.set_xlabel('Time')
ax1.set_ylabel('Magnitude')
ax1.set_title('Wave Plot (Buffered)')

x_instant = np.arange(0, CHUNK, 1)/RATE
line_instant, = ax2.plot(x_instant, np.random.rand(CHUNK), 'r')
ax2.set_ylim(-20000, 20000)
#ax2.set_xlabel('Time')
ax2.set_ylabel('Magnitude')
ax2.set_title('Wave Plot (Instant)')

x_fft = np.linspace(0, RATE, CHUNK)
line_fft, = ax3.loglog(x_fft, np.zeros([CHUNK]), 'r')
ax3.set_xlim(0, RATE/2)
ax3.set_ylim(0.001, 50)
ax3.set_xlabel('Frequency')
ax3.set_ylabel('Magnitude')
ax3.set_title('Fast Fourier Transform')

data_total = np.zeros([CHUNK*multiplier])

while True:
#    data = stream.read(CHUNK)
    data = stream.read(CHUNK, exception_on_overflow=False)

    data_int = np.fromstring(data, 'int16')
    data_total = np.append(data_total[CHUNK-1:-1], data_int)
    line_buffer.set_data(np.arange(0, len(data_total), 1)/RATE, data_total)
    
    line_instant.set_data(np.arange(0, len(data_int), 1)/RATE, data_int)
    
    y_fft = fft(data_int)
    line_fft.set_ydata(gaussian_filter1d(np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK), sigma=2))
    
    fig.canvas.draw()
    fig.canvas.flush_events()


stream.stop_stream()
stream.close()