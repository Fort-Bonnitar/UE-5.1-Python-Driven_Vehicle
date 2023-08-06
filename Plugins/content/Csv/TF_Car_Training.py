import tensorflow as tf
from tensorflow import keras
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
from keras import regularizers







# importing data
df = pd.read_csv('player_mimic.csv')

  


# Defining ins and outs
X= df.drop(['input_throttle'], axis=1)
ys= df['input_steering']
yt= df['input_throttle']
  


#Throttle Split Data
Xt_train, Xt_test, yt_train, yt_test = train_test_split(X,yt,
                                                    random_state=104, 
                                                    test_size=0.25, 
                                                    shuffle=True)


# Steering Spit Data
Xs_train, Xs_test, ys_train, ys_test = train_test_split(X,ys,
                                                    random_state=104, 
                                                    test_size=0.25, 
                                                    shuffle=True)







#   kernel_regularizer=regularizers.l2(0.01)
#can Add dropout after each layer: 
# keras.layers.Dropout(0.2),
#  keras.layers.BatchNormalization(),

s_model = keras.models.Sequential([
                                    keras.layers.Dense(10, input_shape=(5,)),
                                    keras.layers.BatchNormalization(),
                                    keras.layers.Dense(254),
                                    keras.layers.BatchNormalization(),
                                    keras.layers.Dense(1)
                                ])




s_model.compile(optimizer='adam',
                loss='hinge',
                metrics=['accuracy'])

s_model.fit(Xt_train, yt_train, epochs=1000)
s_model.evaluate(Xt_test,  yt_test)