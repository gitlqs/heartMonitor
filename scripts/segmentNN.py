# -*- coding: utf-8 -*-
import librosa
import numpy as np
import pandas as pd
#from librosa import display

from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.layers import InputLayer, Conv1D, Dense, Flatten, MaxPool1D
from tensorflow.keras.models import Sequential


temp = pd.read_csv('dataset/datasetA/Atraining_normal_seg.csv')
#data, sampling_rate = librosa.load('dataset/datasetA/Atraining_normal/201102081321.wav', sr=44100 )

data_x = []
data_y = []
for j in range(temp.shape[0]):
   for i in range(1, temp.shape[1] - 1):
     try: 
       data, sampling_rate = librosa.load('dataset/datasetA/Atraining_normal/'+ temp.iloc[j, 0].split('.')[0] +'.wav', sr=44100)
       temp_data = data[int(temp.iloc[j, i]):int(temp.iloc[j, i+1])]
       temp_label = temp.iloc[:, i].name.split('.')[0]
 
       data_x.append(temp_data)
       data_y.append(temp_label)
     except:
       pass
   
data_x = pad_sequences(data_x, maxlen=5000, dtype='float', padding='post', truncating='post', value=0.)
data_x = data_x / np.max(data_x)

data_x = data_x[:,:,np.newaxis]
data_y = pd.Series(data_y)
data_y.value_counts()

data_y = data_y.map({'S1':0, 'S2':1}).values



model = Sequential()

model.add(InputLayer(input_shape=data_x.shape[1:]))

model.add(Conv1D(filters=50, kernel_size=10, activation='relu'))
model.add(MaxPool1D(strides=8))
model.add(Conv1D(filters=50, kernel_size=10, activation='relu'))
model.add(MaxPool1D(strides=8))
model.add(Flatten())
model.add(Dense(units=1, activation='softmax'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(data_x, data_y, batch_size=32, epochs=5)
