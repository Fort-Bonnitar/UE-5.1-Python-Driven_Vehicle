import pandas as pd 
import numpy as np 
from sklearn import linear_model
import pickle




data = pd.read_csv('player_mimic.csv')


X = data.drop(['input_steering','input_throttle'], axis=1)

# Create a model for input_steering
model_steering = linear_model.LinearRegression()
y_steering = data['input_steering']
model_steering.fit(X, y_steering)


# Create a model for input_throttle
model_throttle = linear_model.LinearRegression()
y_throttle = data['input_throttle']
model_throttle.fit(X, y_throttle)







# Save model_steering
with open('./Models/model_steering.pkl', 'wb') as f:
    pickle.dump(model_steering, f)

# Save model_throttle
with open('./Models/model_throttle.pkl', 'wb') as f:
    pickle.dump(model_throttle, f)



# import pickle

# # Load model_steering
# with open('./Models/model_steering.pkl', 'rb') as f:
#     model_steering = pickle.load(f)

# # Load model_throttle
# with open('./Models/model_throttle.pkl', 'rb') as f:
#     model_throttle = pickle.load(f)
