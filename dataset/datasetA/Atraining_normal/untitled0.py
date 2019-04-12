#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:17:56 2019

@author: qiushili
"""

import wave
import numpy as np
import matplotlib.pyplot as plt

wf = wave.open('201101070538.wav', 'rb')
a = wf.readframes(-1)
a = np.fromstring(a, 'Int16')
#signal = signal[::10]

plt.plot(a)





