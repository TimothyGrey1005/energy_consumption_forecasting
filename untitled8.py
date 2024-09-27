# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SkcwID3qskO-nBSMjigB5pgD7OhYElVb
"""

# Step 1: Import necessary libraries
import pandas as pd
from google.colab import files

# Step 2: Upload the 'submission.csv' file manually
uploaded = files.upload()  # You will be prompted to upload the 'submission.csv' file

# Installing packages
!pip install watermark

# Commented out IPython magic to ensure Python compatibility.
# Import of libraries

# System libraries
import re
import unicodedata
import itertools

# Library for file manipulation
import pandas as pd
import numpy as np
import pandas

# Data visualization
import seaborn as sns
import matplotlib.pylab as pl
import matplotlib as m
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib import pyplot as plt

# Normalization
from sklearn.preprocessing import MinMaxScaler

# Model train test
from sklearn.model_selection import train_test_split

# ANN
import keras
import tensorflow
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout

# Configuration for graph width and layout
sns.set_theme(style='whitegrid')
palette='viridis'

# Warnings remove alerts
import warnings
warnings.filterwarnings("ignore")

# Python version
from platform import python_version
print('Python version in this Jupyter Notebook:', python_version())

# Load library versions
import watermark

# Library versions
# %reload_ext watermark
# %watermark -a "Library versions" --iversions

# Viewing first 5 data
df = pd.read_csv('Complete_South_African_Energy_Consumption.csv.xls')
df.head(5)

# Viewing 5 latest data
df.tail()

# Viewing rows and columns
df.shape

# Info data
df.info()

# Type data
df.dtypes

"""# Part 3 - Exploratory data analysis"""

def create_time_features(df, datetime_col):

    # Convert the datetime column to datetime format if not already in that format
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    # Create new columns for various time features
    df['hour'] = df[datetime_col].dt.hour
    df['day_of_week'] = df[datetime_col].dt.dayofweek
    df['quarter'] = df[datetime_col].dt.quarter
    df['month'] = df[datetime_col].dt.month
    df['year'] = df[datetime_col].dt.year
    df['day_of_year'] = df[datetime_col].dt.dayofyear

    return df

# Example usage:
# Add time features to the DataFrame `df` based on the 'DateTime' column
df = create_time_features(df, 'DateTime')
df

# Generate descriptive statistics and transpose the result for better readability
df.describe().T

"""

    2. Temporal Analysis - Visualization of Temporal Trends

Analyze how Consumption and Production variables evolve over time
"""

# Convert the index to a datetime format if it's not already
df.index = pd.to_datetime(df.index)

plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Consumption'], label='Consumption', color='blue', alpha=0.7, linewidth=2)
plt.plot(df.index, df['Production'], label='Production', color='orange', alpha=0.7, linewidth=2)
plt.title('Electricity Consumption and Production Over Time', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('MW', fontsize=14)
plt.legend(loc='upper right', fontsize=12)
plt.grid(False, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Index date
df.index = pd.to_datetime(df.index)

# Assuming df.index is already in datetime format
plt.figure(figsize=(14, 7))

# Plot Consumption
plt.subplot(2, 1, 1)
plt.plot(df.index, df['Consumption'], label='Consumption', color='blue', alpha=0.7, linewidth=2)
plt.title('Electricity Consumption Over Time')
plt.xlabel('Date')
plt.ylabel('MW')
plt.grid(False, linestyle='--', alpha=0.6)

# Plot Production
plt.subplot(2, 1, 2)
plt.plot(df.index, df['Production'], label='Production', color='orange', alpha=0.7, linewidth=2)
plt.title('Electricity Production Over Time')
plt.xlabel('Date')
plt.ylabel('MW')
plt.grid(False, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

"""- **2.1 Seasonality and Cycles**

Identify seasonal patterns, such as daily, weekly or seasonal variations.
"""

# Consumption per hour
plt.figure(figsize=(14, 7))
df.groupby('hour')['Consumption'].mean().plot(color='blue', linewidth=2, marker='o')
plt.title('Average Hourly Electricity Consumption', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=14)
plt.ylabel('Average Consumption (MW)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(range(0, 24, 2))  # Show ticks every 2 hours
plt.tight_layout()
plt.show()

# Consumption by day of the week
plt.figure(figsize=(14, 7))
df.groupby('day_of_week')['Consumption'].mean().plot(color='green', linewidth=2, marker='o')
plt.title('Average Daily Electricity Consumption', fontsize=16)
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('Average Consumption (MW)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.tight_layout()
plt.show()

# Consumption per month
plt.figure(figsize=(14, 7))
df.groupby('month')['Consumption'].mean().plot(color='orange', linewidth=2, marker='o')
plt.title('Average Monthly Electricity Consumption', fontsize=16)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Average Consumption (MW)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.show()

"""**3. Correlation Analysis**

- Correlation between Variables
- Analyze the correlation between the different sources of energy production and consumption.
"""

corr_matrix = df[['Consumption', 'Production', 'Water', 'Wind', 'Hydroelectric', 'Oil and Gas', 'Coal', 'Solar']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Define figure and grid size
fig, axes = plt.subplots(3, 3, figsize=(18, 14))
fig.suptitle('Distribution of Electricity Variables', fontsize=16)

# Define variables to plot and their corresponding titles
variables = ['Consumption', 'Production', 'Water', 'Wind', 'Hydroelectric', 'Oil and Gas', 'Coal', 'Solar']
titles = ['Consumption', 'Production', 'Water', 'Wind', 'Hydroelectric', 'Oil and Gas', 'Coal', 'Solar']

# Loop through variables and plot them
for i, ax in enumerate(axes.flatten()):
    if i < len(variables):
        df[variables[i]].hist(ax=ax, bins=30, color='steelblue', edgecolor='black')
        ax.set_title(titles[i])
        ax.set_xlabel(f'{titles[i]} (MW)')
        ax.set_ylabel('Frequency')
    else:
        fig.delaxes(ax)  # Remove empty subplots

plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for the suptitle
plt.show()

# Ensure the datetime index is correctly formatted
df.index = pd.to_datetime(df.index)

# Calculate peak consumption based on a quantile threshold
df['peak_consumption'] = df['Consumption'] > df['Consumption'].quantile(0.95)

plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Consumption'], label='Consumption', color='skyblue', linewidth=2)
plt.scatter(df[df['peak_consumption']].index, df[df['peak_consumption']]['Consumption'], color='red', s=20, label='Peak Consumption')

# Add title and labels
plt.title('Electricity Consumption with Peaks Highlighted', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Consumption (MW)', fontsize=14)

# Add grid lines for clarity
plt.grid(True, linestyle='--', alpha=0.7)

# Enhance legend and layout
plt.legend(loc='upper right', fontsize=12)
plt.tight_layout()

plt.show()

# Ensure the datetime index is correctly formatted
df.index = pd.to_datetime(df.index)

# Calculate the net import/export
df['import_export'] = df['Production'] - df['Consumption']

# Plot with improvements
plt.figure(figsize=(18, 8))
plt.plot(df.index, df['import_export'], color='dodgerblue', linewidth=1.5, alpha=0.8)
plt.axhline(0, color='black', linestyle='--', linewidth=2)
plt.title('Electricity Import vs Export', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Net Production - Consumption (MW)', fontsize=14)

# Add grid for better readability
plt.grid(False, linestyle='--', alpha=0.7)

# Use a tight layout
plt.tight_layout()
plt.show()

for source in ['Water', 'Wind', 'Hydroelectric', 'Oil and Gas', 'Coal', 'Solar']:
    df[f'{source}_fraction'] = df[source] / df['Production']

df['consumption_production_ratio'] = df['Consumption'] / df['Production']
df['renewable_production'] = df[['Wind', 'Hydroelectric', 'Solar']].sum(axis=1)
df['non_renewable_production'] = df[['Water', 'Oil and Gas', 'Coal']].sum(axis=1)
df['renewable_fraction'] = df['renewable_production'] / df['Production']

df = df.rename(columns={'DateTime': 'date_time',
                        'Consumption': 'consumption',
                        'Production': 'production',
                        'Water': 'water',
                        'Wind': 'wind',
                        'Hydroelectric': 'hydroelectric',
                        'Oil and Gas': 'oil_and_gas',
                        'Coal': 'coal',
                        'Solar': 'solar',
                        'peak_consumption': 'peak_consumption',
                        'import_export': 'import_export',
                        'Water_fraction': 'water_fraction',
                        'Wind_fraction': 'wind_fraction',
                        'Hydroelectric_fraction': 'hydroelectric_fraction',
                        'Oil and Gas_fraction': 'oil_and_gas_fraction',
                        'Coal_fraction': 'coal_fraction',
                        'Solar_fraction': 'solar_fraction',
                        'consumption_production_ratio': 'consumption_production_ratio',
                        'renewable_production': 'renewable_production',
                        'non_renewable_production': 'non_renewable_production',
                        'renewable_fraction': 'renewable_fraction',
                        'hour': 'hour',
                        'day_of_week': 'day_of_week',
                        'quarter': 'quarter',
                        'month': 'month',
                        'year': 'year',
                        'day_of_year': 'day_of_year'})

# Visualizando dataset
df.info()

"""# Part 3.1 - Time series analysis"""

# Define the energy sources of interest
energy_sources = ['oil_and_gas', 'coal', 'hydroelectric']

# Create subplots for the selected energy sources
fig, axes = plt.subplots(nrows=len(energy_sources), ncols=1, figsize=(14, 7), sharex=True)

# Plot each energy source in its own subplot
for i, source in enumerate(energy_sources):
    axes[i].plot(df.index, df[source], label=source)
    axes[i].set_ylabel('energy sources')
    axes[i].set_title(f'{source} energy sources')
    axes[i].grid(False)

# Set common x-axis label and adjust layout
plt.xlabel('Date Time')
plt.tight_layout()
plt.show()

from pandas.plotting import autocorrelation_plot

# Select the time series of interest, in this case, 'Consumption'
# 'consumption_series' will store the data from the 'consumption' column of the DataFrame 'df'
consumption_series = df['consumption']

# Create a new figure with a specified size for the autocorrelation plot
plt.figure(figsize=(12, 6))

# Generate and plot the autocorrelation of the 'consumption_series'
autocorrelation_plot(consumption_series)

# Add a title to the plot to describe its content
plt.title('Autocorrelation Plot of Electricity Consumption')

# Display the plot
plt.show()

from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt

# Autocorrelation Function (ACF) for Oil and Gas Production

# Create a figure with specified size for the ACF plot
plt.figure(figsize=(12, 6))

# Generate the ACF plot for 'oil_and_gas_fraction' column in the DataFrame 'df'
# 'lags=50' specifies that the autocorrelation should be calculated up to 50 lags
plot_acf(df.oil_and_gas_fraction, lags=50)  # Modify the number of lags as needed

# Add a title to the plot to describe its content
plt.title('ACF Plot of Oil and Gas Production')

# Display the plot
plt.show()

# Autocorrelation Function (ACF) for Hydroelectric Production

# Create another figure with the same size for the ACF plot
plt.figure(figsize=(12, 6))

# Generate the ACF plot for 'hydroelectric_fraction' column in the DataFrame 'df'
# 'lags=50' specifies that the autocorrelation should be calculated up to 50 lags
plot_acf(df.hydroelectric_fraction, lags=50)  # Modify the number of lags as needed

# Add a title to the plot to describe its content
plt.title('ACF Plot of Hydroelectric Production')

# Display the plot
plt.show()

"""# Part 4 - Train Test Split"""

# Define the feature matrix 'X' and the target variable 'y' for a machine learning model

# 'X' is the feature matrix that includes the following columns from the DataFrame 'df':
# 'hour': The hour of the day (0-23)
# 'day_of_week': The day of the week (0=Monday, 6=Sunday)
# 'quarter': The quarter of the year (1-4)
# 'month': The month of the year (1-12)
# 'year': The year component of the date

# 'day_of_year': The day of the year (1-365/366)
X = df[['hour', 'day_of_week', 'quarter', 'month', 'year', 'day_of_year']]

# 'y' is the target variable that represents the electricity consumption, which the model aims to predict.
y = df['consumption']

# Viewing Rows and Columns x
X.shape

# Viewing Rows and Columns y
y.shape

"""# Part 5 - Preprocessing"""

from sklearn.preprocessing import MinMaxScaler

# Initialize MinMaxScaler for both features (X) and target variable (y)
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

# Scale the feature matrix 'X' using MinMaxScaler
# This transforms each feature in 'X' to a range between 0 and 1.
# 'X_scaled' will contain the scaled version of 'X'.
X_scaled = scaler_X.fit_transform(X)

# Scale the target variable 'y' using MinMaxScaler
# Since 'y' is a 1-dimensional array, it is reshaped to a 2-dimensional array before scaling.
# 'y_scaled' will contain the scaled version of 'y' with values between 0 and 1.
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

def create_sequences(X, y, seq_length):
    X_seq, y_seq = [], []

    # Iterate over the length of X minus the sequence length
    for i in range(len(X) - seq_length):
        # Append a sequence of length `seq_length` from X to X_seq
        X_seq.append(X[i:i+seq_length])

        # Append the corresponding target value from y to y_seq
        y_seq.append(y[i+seq_length])

    # Convert the lists to numpy arrays for efficient computation and return them
    return np.array(X_seq), np.array(y_seq)

# Define the sequence length for time series prediction
SEQ_LENGTH = 24  # Example: Use the previous 24 hours to predict the next hour

# Create sequences using the scaled feature matrix X_scaled and target array y_scaled
X_seq, y_seq = create_sequences(X_scaled, y_scaled, SEQ_LENGTH)

"""# Part 6 - Model Building"""

from sklearn.model_selection import train_test_split

# Split the sequences into training and testing sets

# X_seq: The 3D array containing sequences of features (created earlier using the create_sequences function).
# y_seq: The 1D array containing the target values corresponding to each sequence in X_seq.

# Parameters:
# - test_size=0.2: Specifies that 20% of the data should be allocated to the test set, and 80% to the training set.
# - random_state=42: Ensures reproducibility by setting a seed for the random number generator.
# - shuffle=False: Prevents shuffling of the data before splitting, which is important for time series data to maintain the temporal order.

X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42, shuffle=False)

"""### 6.1 - LSTM"""

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

# Assuming 'data' is loaded and you've created sequences already stored in X_train, y_train, X_test, y_test

# Scaling the features
feature_scaler = MinMaxScaler()
X_train_scaled = feature_scaler.fit_transform(X_train.reshape(X_train.shape[0], -1))  # Flatten and then scale
X_train_scaled = X_train_scaled.reshape(X_train.shape)  # Reshape back to original shape (samples, time steps, features)

X_test_scaled = feature_scaler.transform(X_test.reshape(X_test.shape[0], -1))
X_test_scaled = X_test_scaled.reshape(X_test.shape)  # Ensure this is also (samples, time steps, features)

# Scaling the target
target_scaler = MinMaxScaler()
y_train_scaled = target_scaler.fit_transform(y_train)
y_test_scaled = target_scaler.transform(y_test)

# Build the LSTM model
model = Sequential([
    LSTM(50, input_shape=(X_train_scaled.shape[1], X_train_scaled.shape[2]), return_sequences=True),
    LSTM(50, return_sequences=False),
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train_scaled, y_train_scaled, epochs=10, validation_split=0.2, batch_size=32, verbose=1)

# Predict using the trained model
predictions = model.predict(X_test_scaled)

# Reverse the scaling of the predictions and actual values to get the original scale
predictions_actual = target_scaler.inverse_transform(predictions)
y_test_actual = target_scaler.inverse_transform(y_test_scaled)

# Plotting and metrics calculations follow
mse = mean_squared_error(y_test_actual, predictions_actual)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_actual, predictions_actual)

print("MSE:", mse)
print("RMSE:", rmse)
print("R²:", r2)

plt.figure(figsize=(10, 5))
plt.plot(y_test_actual, label='Actual')
plt.plot(predictions_actual, label='Predicted')
plt.title('Actual vs Predicted')
plt.xlabel('Time (index)')
plt.ylabel('Target Variable')
plt.legend()
plt.show()

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

# Function to smooth the curve
def smooth_curve(points, factor=0.8):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

# Assume data loading and preprocessing is already done
# Define scalers for input and output
feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

# Plotting the training and validation loss with smoothing
plt.figure(figsize=(10, 6))
smoothed_training_loss = smooth_curve(history.history['loss'])
smoothed_validation_loss = smooth_curve(history.history['val_loss'])

plt.plot(smoothed_training_loss, label='Training Loss (Smoothed)', color='blue', linestyle='-')
plt.plot(smoothed_validation_loss, label='Validation Loss (Smoothed)', color='orange', linestyle='--')

min_val_loss_idx = np.argmin(history.history['val_loss'])
plt.scatter(min_val_loss_idx, history.history['val_loss'][min_val_loss_idx], color='red', s=50, label='Min Validation Loss')

plt.grid(True)
plt.title('Training and Validation Loss - LSTM', fontsize=16)
plt.xlabel('Epochs', fontsize=14)
plt.ylabel('Loss', fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

"""### 6.2 - Decision Trees"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

# Assuming 'data' is loaded and you've created sequences already stored in X_train, y_train, X_test, y_test

# Flatten the inputs for Decision Tree, as it does not require sequence data like LSTM
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Decision Trees do not require feature scaling, but using scaled data for consistency
feature_scaler = MinMaxScaler()
X_train_scaled = feature_scaler.fit_transform(X_train_flat)
X_test_scaled = feature_scaler.transform(X_test_flat)

# Scaling the target (if needed for consistency in comparison)
target_scaler = MinMaxScaler()
y_train_scaled = target_scaler.fit_transform(y_train)
y_test_scaled = target_scaler.transform(y_test)

# Build the Decision Tree model
dt_regressor = DecisionTreeRegressor(random_state=42)
dt_regressor.fit(X_train_scaled, y_train_scaled.ravel())  # Flatten if needed

# Predict using the trained model
predictions_dt = dt_regressor.predict(X_test_scaled)

# Reverse the scaling of the predictions and actual values to get the original scale
predictions_dt_actual = target_scaler.inverse_transform(predictions_dt.reshape(-1, 1))
y_test_actual = target_scaler.inverse_transform(y_test_scaled)

# Calculate evaluation metrics
mse_dt = mean_squared_error(y_test_actual, predictions_dt_actual)
rmse_dt = np.sqrt(mse_dt)
r2_dt = r2_score(y_test_actual, predictions_dt_actual)

# Output the metrics
print("Decision Tree - MSE:", mse_dt)
print("Decision Tree - RMSE:", rmse_dt)
print("Decision Tree - R²:", r2_dt)

# Plot actual vs predicted values
plt.figure(figsize=(10, 5))
plt.plot(y_test_actual, label='Actual')
plt.plot(predictions_dt_actual, label='Predicted')
plt.title('Decision Tree - Actual vs Predicted')
plt.xlabel('Time (index)')
plt.ylabel('Target Variable')
plt.legend()
plt.show()

"""### 6.3 - XGBoost"""

import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Assuming 'data' is loaded and matrices are stored in X_train, y_train, X_test, y_test

# Flatten inputs since XGBoost does not require sequence data
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Split the training data to create a validation set
X_train_part, X_val, y_train_part, y_val = train_test_split(X_train_flat, y_train, test_size=0.2, random_state=42)

# Optionally scale features
feature_scaler = MinMaxScaler()
X_train_scaled = feature_scaler.fit_transform(X_train_part)
X_val_scaled = feature_scaler.transform(X_val)
X_test_scaled = feature_scaler.transform(X_test_flat)

# Optionally scale the target for consistent comparison with other models
target_scaler = MinMaxScaler()
y_train_scaled = target_scaler.fit_transform(y_train_part)
y_val_scaled = target_scaler.transform(y_val)

# Initialize XGBoost regressor object with specified parameters
xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                          max_depth = 5, alpha = 10, n_estimators = 100)

# Fit the model
xg_reg.fit(X_train_scaled, y_train_scaled.ravel())

# Predicting on the test set
predictions_xgb = xg_reg.predict(X_test_scaled)

# Reverse the scaling of the predictions and actual values to get the original scale
predictions_xgb_actual = target_scaler.inverse_transform(predictions_xgb.reshape(-1, 1))
y_test_actual = target_scaler.inverse_transform(y_test_scaled)

# Compute and print the performance metrics
mse_xgb = mean_squared_error(y_test_actual, predictions_xgb_actual)
rmse_xgb = np.sqrt(mse_xgb)
r2_xgb = r2_score(y_test_actual, predictions_xgb_actual)
print("XGBoost - MSE:", mse_xgb)
print("XGBoost - RMSE:", rmse_xgb)
print("XGBoost - R²:", r2_xgb)

# Plot actual vs predicted values
plt.figure(figsize=(10, 5))
plt.plot(y_test_actual, label='Actual')
plt.plot(predictions_xgb_actual, label='Predicted')
plt.title('XGBoost - Actual vs Predicted')
plt.xlabel('Time (index)')
plt.ylabel('Target Variable')
plt.legend()
plt.show()

"""### 6.4 - k-NN

```
# This is formatted as code
```


"""

from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Assuming 'data' is loaded and matrices are stored in X_train, y_train, X_test, y_test

# Flatten inputs since k-NN does not require sequence data
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Split the training data to create a validation set
X_train_part, X_val, y_train_part, y_val = train_test_split(X_train_flat, y_train, test_size=0.2, random_state=42)

# Scale features and target using MinMaxScaler for consistency
feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

X_train_scaled = feature_scaler.fit_transform(X_train_part)
X_val_scaled = feature_scaler.transform(X_val)
X_test_scaled = feature_scaler.transform(X_test_flat)

y_train_scaled = target_scaler.fit_transform(y_train_part.reshape(-1, 1))
y_val_scaled = target_scaler.transform(y_val.reshape(-1, 1))

# Initialize k-NN regressor object with specified parameters
knn_reg = KNeighborsRegressor(n_neighbors=5)

# Fit the model
knn_reg.fit(X_train_scaled, y_train_scaled.ravel())

# Predicting on the test set
predictions_knn = knn_reg.predict(X_test_scaled)

# Reverse the scaling of the predictions and actual values to get the original scale
predictions_knn_actual = target_scaler.inverse_transform(predictions_knn.reshape(-1, 1))
y_test_actual = target_scaler.inverse_transform(y_test_scaled)

# Compute and print the performance metrics
mse_knn = mean_squared_error(y_test_actual, predictions_knn_actual)
rmse_knn = np.sqrt(mse_knn)
r2_knn = r2_score(y_test_actual, predictions_knn_actual)
print("k-NN - MSE:", mse_knn)
print("k-NN - RMSE:", rmse_knn)
print("k-NN - R²:", r2_knn)

# Plot actual vs predicted values
plt.figure(figsize=(10, 5))
plt.plot(y_test_actual, label='Actual')
plt.plot(predictions_knn_actual, label='Predicted')
plt.title('k-NN - Actual vs Predicted')
plt.xlabel('Time (index)')
plt.ylabel('Target Variable')
plt.legend()
plt.show()

"""### 6.5 - Random Forest"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Assuming 'data' is loaded and matrices are stored in X_train, y_train, X_test, y_test

# Flatten inputs since Random Forest does not require sequence data
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Split the training data to create a validation set
X_train_part, X_val, y_train_part, y_val = train_test_split(X_train_flat, y_train, test_size=0.2, random_state=42)

# Scale features and target using MinMaxScaler for consistency, though not strictly necessary for Random Forest
feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

X_train_scaled = feature_scaler.fit_transform(X_train_part)
X_val_scaled = feature_scaler.transform(X_val)
X_test_scaled = feature_scaler.transform(X_test_flat)

y_train_scaled = target_scaler.fit_transform(y_train_part.reshape(-1, 1))
y_val_scaled = target_scaler.transform(y_val.reshape(-1, 1))

# Initialize Random Forest regressor object with specified parameters
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)

# Fit the model
rf_reg.fit(X_train_scaled, y_train_scaled.ravel())

# Predicting on the test set
predictions_rf = rf_reg.predict(X_test_scaled)

# Reverse the scaling of the predictions and actual values to get the original scale
predictions_rf_actual = target_scaler.inverse_transform(predictions_rf.reshape(-1, 1))
y_test_actual = target_scaler.inverse_transform(y_test_scaled)

# Compute and print the performance metrics
mse_rf = mean_squared_error(y_test_actual, predictions_rf_actual)
rmse_rf = np.sqrt(mse_rf)
r2_rf = r2_score(y_test_actual, predictions_rf_actual)
print("Random Forest - MSE:", mse_rf)
print("Random Forest - RMSE:", rmse_rf)
print("Random Forest - R²:", r2_rf)

# Plot actual vs predicted values
plt.figure(figsize=(10, 5))
plt.plot(y_test_actual, label='Actual')
plt.plot(predictions_rf_actual, label='Predicted')
plt.title('Random Forest - Actual vs Predicted')
plt.xlabel('Time (index)')
plt.ylabel('Target Variable')
plt.legend()
plt.show()

"""# 7. Model Selection"""

import matplotlib.pyplot as plt
import numpy as np

# Model names
models = ['Random Forest', 'k-NN', 'XGBoost', 'Decision Tree', 'LSTM']

# Performance metrics
mse = [0.007132000758300073, 0.008588763025075524, 0.006085544763402205, 0.008390322727937768, 0.01477788218959075]
rmse = [0.08445117381244664, 0.0926755794428906, 0.07800990170101617, 0.09159870483766551, 0.12156431297708531]
r_squared = [0.7330167379057544, 0.6784834932721377, 0.7721903505600671, 0.6859120171403008, 0.4467965823994392]

x = np.arange(len(models))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width, mse, width, label='MSE')
rects2 = ax.bar(x, rmse, width, label='RMSE')
rects3 = ax.bar(x + width, r_squared, width, label='R²')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Models')
ax.set_title('Comparison of Model Performance')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)

fig.tight_layout()

plt.show()

import pandas as pd

# Creating a DataFrame to store the performance metrics
df = pd.DataFrame({
    'Model': models,
    'MSE': mse,
    'RMSE': rmse,
    'R²': r_squared
})

# Sorting the DataFrame based on R² in descending order to get the best model at the top
df_sorted = df.sort_values(by='R²', ascending=False)

# Display the sorted DataFrame
print("Model Ranking Based on R²:")
print(df_sorted)

# Identify the best overall model
best_model = df_sorted.iloc[0]
print("\nBest Performing Model Overall:")
print(best_model)

"""# 8. Model Optimization"""

!pip install optuna

import xgboost as xgb

dtrain = xgb.DMatrix(X_train_scaled, label=y_train_scaled)
dtest = xgb.DMatrix(X_test_scaled, label=y_test_scaled)

params = {'objective': 'reg:squarederror', 'colsample_bytree': 0.3, 'learning_rate': 0.1,
          'max_depth': 5, 'alpha': 10}

bst = xgb.train(params, dtrain, num_boost_round=100, evals=[(dtest, 'eval')], early_stopping_rounds=10)

import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from google.colab import files

# Step 2: Upload the 'submission.csv' file manually
uploaded = files.upload()  # You will be prompted to upload the 'submission.csv' file

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Hyperparameter grid
param_grid = {
    'max_depth': [3, 4, 5, 6, 7],
    'n_estimators': [100, 200, 300, 400],
    'learning_rate': [0.01, 0.05, 0.1, 0.15],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    'min_child_weight': [1, 2, 3, 4],
    'gamma': [0, 0.1, 0.2, 0.3, 0.4]
}

# Create a random search object
clf = RandomizedSearchCV(
    estimator=xgb.XGBRegressor(objective='reg:squarederror'),
    param_distributions=param_grid,
    n_iter=50,  # Number of parameter settings sampled. Trade-off between runtime vs quality of the solution.
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    cv=3,
    verbose=3,
    random_state=42
)

# Fit the random search model
clf.fit(X_train_scaled, y_train)

# Print best parameters and best score (MSE)
print("Best parameters:", clf.best_params_)
print("Best score (negative MSE):", clf.best_score_)

# Evaluate on the test set
best_estimator = clf.best_estimator_
predictions = best_estimator.predict(X_test_scaled)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

print("Test MSE:", mse)
print("Test RMSE:", rmse)
print("Test R²:", r2)

import matplotlib.pyplot as plt

# Convert the actual values and predictions into compatible formats if necessary
y_test_actual = np.array(y_test)  # Make sure y_test is in the correct format
predictions_actual = predictions  # This should already be an array from the model output

# Creating the plot
plt.figure(figsize=(10, 5))
plt.plot(y_test_actual, label='Actual Values', color='blue', marker='o', linestyle='-', markersize=5)
plt.plot(predictions_actual, label='Predicted Values', color='red', marker='x', linestyle='--', markersize=5)
plt.title('Comparison of Actual and Predicted Values')
plt.xlabel('Index')
plt.ylabel('Target Variable')
plt.legend()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Calculate residuals
residuals = y_test_actual - predictions_actual

# Plotting residuals
plt.figure(figsize=(10, 6))
plt.scatter(y_test_actual, residuals, color='blue', alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residual Plot')
plt.xlabel('Actual Values')
plt.ylabel('Residuals')
plt.show()

# Histogram of residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='blue')
plt.title('Distribution of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

from sklearn.metrics import mean_absolute_error

# Calculate additional metrics
mae = mean_absolute_error(y_test_actual, predictions_actual)
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Coefficient of Determination (R²): {r2}")


# Suggest mitigation strategies
if residuals.var() > 0.05 * residuals.mean():  # Example condition for heteroscedasticity
    print("Model may exhibit heteroscedasticity, suggesting issues with equal variance across data points.")
    print("Consider transforming the target variable or using weighted regression techniques.")
else:
    print("Residuals appear homoscedastic, indicating consistent variance across predictions.")


# Define project success criteria
success_criteria_r2 = 0.95  # Example criterion

if r2 >= success_criteria_r2:
    print(f"Model meets the project's success criterion with an R² of {r2}.")
else:
    print(f"Model fails to meet the success criterion with an R² of {r2}. Consider further optimization.")