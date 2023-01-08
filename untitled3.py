# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rlrvPdmMq8UUyTfePyPhu_gK2FlmKYLY
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
import matplotlib.pyplot as plt
import random
import scipy.stats as stats
import numpy as np
import scipy.stats as st

num_lists = 100000 # Number of lists to generate

# Initialize empty lists for each parameter
S_values = []
K_values = []
R_values = []
t_values = []
sigma_values = []
Pri=[]
# Generate values for each parameter following the specified distributions
for i in range(num_lists):
  S_values.append(stats.gamma.rvs(a=100, scale=1))
  K_values.append(random.uniform(50, 200))
  R_values.append(random.uniform(0.01, 0.18))
  t_values.append(random.choice([0.25, 0.5, 0.75, 1]))
  sigma_values.append(stats.beta.rvs(a=2, b=5) + 0.001)

def black_scholes(S, K, R, t, sigma):
  # Calculate the Black-Scholes price of a European call option
  d1 = (np.log(S / K) + (R + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
  d2 = d1 - sigma * np.sqrt(t)
  call_price = S * st.norm.cdf(d1) - K * np.exp(-R * t) * st.norm.cdf(d2)

for i in range(num_lists):
  d1 = (np.log(S_values[i] / K_values[i]) + (R_values[i] + sigma_values[i]**2 / 2) * t_values[i]) / (sigma_values[i] * np.sqrt(t_values[i]))
  d2 = d1 - sigma_values[i] * np.sqrt(t_values[i])
  call_price = S_values[i] * st.norm.cdf(d1) - K_values[i] * np.exp(-R_values[i] * t_values[i]) * st.norm.cdf(d2)

  Pri.append(call_price)

# Create a dictionary with the data for each column
data = {
    'S': S_values,
    'K': K_values,
    'R': R_values,
    'sigma': sigma_values,
    't': t_values,
    'option_price': Pri
}

# Create the pandas DataFrame
df = pd.DataFrame(data)

df

df.head(10)

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np



# Select the features and target
X = df[['S', 'K', 'R', 'sigma', 't']]
y = df['option_price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
model = RandomForestRegressor(n_estimators=100)

# Train the model on the training data
model.fit(X_train, y_train)



# Make predictions on the testing data
predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
print(f'Test MSE: {mse:.2f}')
# Calculate the mean absolute error
mae = mean_absolute_error(y_test, predictions)
print(f'Test MAE: {mae:.2f}')

# Calculate the residuals
residuals = y_test - predictions

# Plot the residuals as a histogram
plt.hist(residuals, bins=50)
plt.xlabel('Residual')
plt.ylabel('Count')
plt.title('Residual Histogram')
plt.show()

import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error



# Select the features and target
X = df[['S', 'K', 'R', 'sigma', 't']]
y = df['option_price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a decision tree model
model = DecisionTreeRegressor()

# Train the model on the training data
model.fit(X_train, y_train)

# Evaluate the model on the testing data
score = model.score(X_test, y_test)
print(f'Test score: {score:.2f}')

# Make predictions on the testing data
predictions = model.predict(X_test)

# Calculate the mean absolute error
mae = mean_absolute_error(y_test, predictions)
print(f'Test MAE: {mae:.2f}')


mse = mean_squared_error(y_test, predictions)
print(f'Test MSE: {mse:.2f}')
# Calculate the residuals
residuals = y_test - predictions

# Plot the residuals as a histogram
plt.hist(residuals, bins=50)
plt.xlabel('Residual')
plt.ylabel('Count')
plt.title('Residual Histogram')
plt.show()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

# Separate the features and target
X = df.drop("option_price", axis=1)
y = df["option_price"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create the neural network model
model = MLPRegressor(hidden_layer_sizes=(100,100,100), max_iter=10000)

# Train the model on the training data
model.fit(X_train, y_train)

# Evaluate the model on the testing data
accuracy = model.score(X_test, y_test)
print(f'Accuracy: {accuracy:.2f}')

# Make predictions on the testing data
predictions = model.predict(X_test)

# Calculate the mean absolute error
mae = mean_absolute_error(y_test, predictions)
print(f'Test MAE: {mae:.2f}')
# Make predictions on the testing data
predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
print(f'Test MSE: {mse:.2f}')
# Plot the residuals as a histogram
plt.hist(residuals, bins=50)
plt.xlabel('Residual')
plt.ylabel('Count')
plt.title('Residual Histogram')
plt.show()

import xgboost as xgb
from sklearn.metrics import mean_absolute_error

#Split the data into training and testing sets
X = df.drop(columns=['option_price'])
y = df['option_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create the XGBoost model
model = xgb.XGBRegressor(objective='reg:squarederror')

#Train the model
model.fit(X_train, y_train)

#Make predictions on the testing data
predictions = model.predict(X_test)

#Calculate the mean absolute error
mae = mean_absolute_error(y_test, predictions)
print(f'Test MAE: {mae:.2f}')


mse = mean_squared_error(y_test, predictions)
print(f'Test MSE: {mse:.2f}')
# Plot the residuals as a histogram
plt.hist(residuals, bins=50)
plt.xlabel('Residual')
plt.ylabel('Count')
plt.title('Residual Histogram')
plt.show()