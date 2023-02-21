# -*- coding: utf-8 -*-
"""Forecasting DST Index using Machine Learning

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q4wqoQQUVsaQKYRnKKtdMuT8W2GITN2G
"""

# Forecasting DST Index using Machine Learning

# By Emanuel Istratoaie (Student 3rd year FIT, BusEco) 
# and Alina Donea (SoM, DFI) Monash University

# Check to determine if GPU is connected
!nvidia-smi

# Importing libraries needed for the data preprocessing and visualisation
import tensorflow as tf
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the data csv file and read it 
# Change the csv_path to the path 
csv_path = r'/content/drive/MyDrive/Colab Notebooks/DST(Time-Series Format).csv'
df = pd.read_csv(csv_path)
df

# Convert the time to a datetime object
df.index = pd.to_datetime(df["Datetime"], format = '%Y-%m-%d %H:%M:%S')
df[:10]

# Plot the DST Index data
temp = df["DST Index"]
temp.plot()

# Plot a sample of every 100th DST Index, with lines for the mean and standard deviations and all data partitioned into training, validation and testing sets
plt.figure(figsize=(20, 10))
df1 = df[::100]
# print(df1.head())
# print(df.iloc[-1, :])
train, val, test = 3000, 3300, 3783
ax = plt.gca()
ax.plot(df1["DST Index"][:train], label = "Training Set")
ax.plot(df1["DST Index"][train-1:val], label = "Validation Set")
ax.plot(df1["DST Index"][val-1:test], label = "Testing Set")
ax.axhline(y = -15.5015, color = 'k', linestyle = '-')
ax.axhline(y = -15.5015+22.89183, color = 'r', linestyle = '-')
ax.axhline(y = -15.5015-22.89183, color = 'r', linestyle = '-')
ax.legend(loc="lower right")
start, end = pd.to_datetime("1975-01-01 00:00:00"), pd.to_datetime("2018-02-28 23:00:00")
ax.set_xlim(start, end)
plt.show()

#Function for preprocessing the data by convertng the dataframe to numpy arrays
def df_to_xy(df, BATCH_SIZE = 5):
  df_as_np =  df.to_numpy()
  x = []
  y = []
  for i in range(len(df_as_np)-BATCH_SIZE):
    row = [[a] for a in df_as_np[i:i+BATCH_SIZE]]
    x.append(row)
    label = df_as_np[i+BATCH_SIZE]
    y.append(label)
  return np.array(x), np.array(y)

#Setting the batch size to 5 and creating numpy arrays containing the data before outputing the shape of the arrays
BATCH_SIZE = 5
x,y = df_to_xy(temp, BATCH_SIZE)
x.shape, y.shape

# Partitioning the data into training, validation and testing arrays before outputing their shape
x_train, y_train = x[:300000], y[:300000]
x_val, y_val = x[300000:330000], y[300000:330000]
x_test, y_test = x[330000:], y[330000:]
x_train.shape, y_train.shape, x_val.shape, y_val.shape, x_test.shape, y_test.shape

# Importing the libraries needed for the implementation and training of the model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError, mean_squared_error
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

#Define the single LSTM model
model1 = Sequential()
model1.add(InputLayer((BATCH_SIZE,1)))
model1.add(LSTM(64))
model1.add(Dense(8, 'relu'))
model1.add(Dense(1, 'linear'))

model1.summary()

# Define the model checkpoint
cp1 = ModelCheckpoint('model1/', save_best_only=True)

# Compile the model with the Adam optimizer and the Mean Squared Error loss function
model1.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics=[RootMeanSquaredError()])

# Train the model with the model checkpoint callbacks
history = model1.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10, callbacks=[cp1])

# Record the RMSE at each epoch
train_rmse = history.history['root_mean_squared_error']

# Plot the RMSE values
plt.plot(train_rmse, label='Training RMSE')
plt.ylabel('RMSE')
plt.xlabel('Epoch')
plt.legend()
plt.show()

# Record the Loss at each epoch
train_rmse = history.history['loss']

# Plot the Loss values
plt.plot(train_rmse, label='Training Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()

# Load the best model into mod1
mod1 = load_model('model1/')

# Add the predictions to a dataframe
test_predictions = mod1.predict(x_test).flatten()
test_results = pd.DataFrame(data={'Test Predictions':test_predictions, 'Actuals':y_test})

# Plot the predictions for the first 100 datapoints of the testing set
plt.plot(test_results['Test Predictions'][:100], label = "Predicted")
plt.plot(test_results['Actuals'][:100], label = "Actual")
plt.legend(loc="upper right")

# Define the double LSTM model
model2 = Sequential()
model2.add(LSTM(50, return_sequences=True, input_shape=(BATCH_SIZE,1)))
model2.add(LSTM(50, return_sequences=False))
model2.add(Dense(25))
model2.add(Dense(1))

model2.summary()

# Define the model checkpoint
cp2 = ModelCheckpoint('model2/', save_best_only= True)

# Compile the model with the Adam optimizer and the Mean Squared Error loss function
model2.compile(loss = MeanSquaredError(), optimizer= Adam(learning_rate=0.0001), metrics = [RootMeanSquaredError()])

# Train the model with the model checkpoint callbacks
model2.fit(x_train, y_train, validation_data=(x_val, y_val), epochs = 10, callbacks = [cp2])

# Load the best model into mod2
mod2 = load_model('model2/')

# Add the predictions to a dataframe
test_predictions = mod2.predict(x_test).flatten()
test_results = pd.DataFrame(data={'Test Predictions':test_predictions, 'Actuals':y_test})

# Plot the predictions for the first 100 datapoints of the testing set
plt.plot(test_results['Test Predictions'][:100], label = "Predicted")
plt.plot(test_results['Actuals'][:100], label = "Actual")
plt.legend(loc="upper right")

# Define the 1D CNN model
model3 = Sequential()
model3.add(InputLayer((BATCH_SIZE,1)))
model3.add(Conv1D(64, kernel_size = 2))
model3.add(Flatten())
model3.add(Dense(8, 'relu'))
model3.add(Dense(1, 'linear'))

model3.summary()

# Define the model checkpoint
cp3 = ModelCheckpoint('model3/', save_best_only= True)

# Compile the model with the Adam optimizer and the Mean Squared Error loss function
model3.compile(loss = MeanSquaredError(), optimizer= Adam(learning_rate=0.0001), metrics = [RootMeanSquaredError()])

# Train the model with the model checkpoint callbacks
model3.fit(x_train, y_train, validation_data=(x_val, y_val), epochs = 10, callbacks = [cp3])

# Load the best model into mod3
mod3 = load_model('model3/')

# Add the predictions to a dataframe
test_predictions = mod3.predict(x_test).flatten()
test_results = pd.DataFrame(data={'Test Predictions':test_predictions, 'Actuals':y_test})

# Plot the predictions for the first 100 datapoints of the testing set
plt.plot(test_results['Test Predictions'][:100], label = "Predicted")
plt.plot(test_results['Actuals'][:100], label = "Actual")
plt.legend(loc="upper right")

# Define the GRU model
model4 = Sequential()
model4.add(InputLayer((BATCH_SIZE,1)))
model4.add(GRU(64))
model4.add(Flatten())
model4.add(Dense(8, 'relu'))
model4.add(Dense(1, 'linear'))

model4.summary()

# Define the model checkpoint
cp4 = ModelCheckpoint('model4/', save_best_only= True)

# Compile the model with the Adam optimizer and the Mean Squared Error loss function
model4.compile(loss = MeanSquaredError(), optimizer= Adam(learning_rate=0.0001), metrics = [RootMeanSquaredError()])

# Train the model with the model checkpoint callbacks
model4.fit(x_train, y_train, validation_data=(x_val, y_val), epochs = 10, callbacks = [cp4])

# Load the best model into mod4
mod4 = load_model('model1/')

# Add the predictions to a dataframe
test_predictions = mod4.predict(x_test).flatten()
test_results = pd.DataFrame(data={'Test Predictions':test_predictions, 'Actuals':y_test})

# Plot the predictions for the first 100 datapoints of the testing set
plt.plot(test_results['Test Predictions'][:100], label = "Predicted")
plt.plot(test_results['Actuals'][:100], label = "Actual")
plt.legend(loc="upper right")

# Use all models to forecast testing data
test_predictions1 = model1.predict(x_test).flatten()
test_predictions2 = model2.predict(x_test).flatten()
test_predictions3 = model3.predict(x_test).flatten()
test_predictions4 = model4.predict(x_test).flatten()
test_results = pd.DataFrame(data={'Single LSTM Predictions':test_predictions1, 'Double LSTM Predictions':test_predictions2, '1-D CNN Predictions':test_predictions3, 'GRU Predictions':test_predictions4, 'Actuals':y_test})

# Plot the predictions of each model on the first dp (100) data points of the testing data
plt.figure(figsize=(20,10))
dp = 100
plt.plot(test_results['Single LSTM Predictions'][:dp], label = "Single LSTM Predictions")
plt.plot(test_results['Double LSTM Predictions'][:dp], label = "Double LSTM Predictions")
plt.plot(test_results['1-D CNN Predictions'][:dp], label = "1-D CNN Predictions")
plt.plot(test_results['GRU Predictions'][:dp], label = "GRU Predictions")
plt.plot(test_results['Actuals'][:dp], label = "Actual")
plt.legend(loc="upper right")

# The following cells of code are intended to be run independently for testing various model configurations conveniently
# Please note that "Model Implementation" and "Model Training" cells need to be run consecutively each time a hyperparameter is adjusted to avoid training the same model

# Data Preparation:

# Import statements
import tensorflow as tf
import os
import pandas as pd
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam

from google.colab import drive

# Read the data file
# Change the csv_path to the path 
csv_path = r'/content/drive/MyDrive/Colab Notebooks/DST(Time-Series Format).csv'
df = pd.read_csv(csv_path)

# Convert time series to Datetime object
df.index = pd.to_datetime(df["Datetime"], format = '%Y-%m-%d %H:%M:%S')
df = df['DST Index']

# Define a function that preprocesses the data
def df_to_xy(df, BATCH_SIZE = 5):
  df_as_np =  df.to_numpy()
  x = []
  y = []
  for i in range(len(df_as_np)-BATCH_SIZE):
    row = [[a] for a in df_as_np[i:i+BATCH_SIZE]]
    x.append(row)
    label = df_as_np[i+BATCH_SIZE]
    y.append(label)
  return np.array(x), np.array(y)

# Model Creation:

#Setting the batch size to 5 and creating numpy arrays containing the data
BATCH_SIZE = 5
x,y = df_to_xy(df, BATCH_SIZE)

# Partitioning the data into training, validation and testing arrays before outputing their shape
x_train, y_train = x[:300000], y[:300000]
x_val, y_val = x[300000:330000], y[300000:330000]
x_test, y_test = x[330000:], y[330000:]

# Creating the model
model1 = Sequential()
# Uncomment a block of the following code to test a model


# model1.add(InputLayer((BATCH_SIZE,1)))
# model1.add(LSTM(64))
# model1.add(Dense(8, 'relu'))
# model1.add(Dense(1, 'linear'))


# model1.add(LSTM(50, return_sequences=True, input_shape=(BATCH_SIZE,1)))
# model1.add(LSTM(50, return_sequences=False))
# model1.add(Dense(25))
# model1.add(Dense(1))


# model1.add(InputLayer((BATCH_SIZE,1)))
# model1.add(Conv1D(64, kernel_size = 2))
# model1.add(Flatten())
# model1.add(Dense(8, 'relu'))
# model1.add(Dense(1, 'linear'))


# model1.add(InputLayer((BATCH_SIZE,1)))
# model1.add(GRU(64))
# model1.add(Flatten())
# model1.add(Dense(8, 'relu'))
# model1.add(Dense(1, 'linear'))


# model1.add(InputLayer((BATCH_SIZE,1)))
# model1.add(Conv1D(64, kernel_size = 2))
# model1.add(Conv1D(64, kernel_size = 2))
# model1.add(Conv1D(64, kernel_size = 2))
# model1.add(Flatten())
# model1.add(Dense(8, 'relu'))
# model1.add(Dense(1, 'linear'))


model1.summary()

# Model Training:

# Define the model checkpoint
cp = ModelCheckpoint('model1/', save_best_only= True)

# Compile the model with the Adam optimizer and the Mean Squared Error loss function
model1.compile(loss = MeanSquaredError(), optimizer= Adam(learning_rate=0.0001), metrics = [RootMeanSquaredError()])

# Train the model with the model checkpoint callbacks
model1.fit(x_train, y_train, validation_data=(x_val, y_val), epochs = 10, callbacks = [cp])

# Load the best model into mod1
mod1 = load_model('model1/')

# Add the predictions to a dataframe
test_predictions = mod1.predict(x_test).flatten()
test_results = pd.DataFrame(data={'Test Predictions':test_predictions, 'Actuals':y_test})

# Plot the predictions for the first 100 datapoints of the testing set
plt.figure(figsize=(20,10))
plt.plot(test_results['Test Predictions'][:100], label = "Predicted")
plt.plot(test_results['Actuals'][:100], label = "Actual")
plt.legend(loc="upper right")
