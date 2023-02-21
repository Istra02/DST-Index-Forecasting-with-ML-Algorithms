# Forecasting the DST Index using Machine Learning
This project implements multiple machine learning model to forecast the DST (Disturbance Storm-Time) Index. The DST Index is a measure of the geomagnetic activity of the Earth's magnetic field, and it is used to study space weather phenomena. The models are built using TensorFlow and Keras libraries. The code is structured for efficient optimisation and comparison of Neural Network models such as the Long Short Term Memory (LSTM), 1-Dimensional Convolutional Neural Network and the Gated Reccurent Unit (GRU). The aim of the models is to predict the next data point given a batch of historic data points. 

# Contributors
Emanuel Istratoaie (Student 3rd year FIT, BusEco), Monash University

Alina Donea (SoM, DFI), Monash University

# Prerequisites
-Python IDE, Jupyter Notebooks or Google Colab

-Python 3

-TensorFlow

-Pandas

-Numpy

-Matplotlib


# Running the Code
To run the code, you have three options:
1. Run .py file on local machine
    1. Clone this repository to your local machine.
    2. Install the required libraries.
    3. Run the Python file "DST-Forecasting-ML.ipynb".

2. Run .ipynb file on local machine
    1. Clone this repository to your local machine.
    2. Install the required libraries.
    3. Run the Jupyter notebook "DST-Forecasting-ML.ipynb".

3. Run .ipynb file using Google Colab
    1. Download the "DST(Time-Series Format).csv" file
    2. Open the .ipynb file in Github
    3. Click on "Open in Colab" at the top of the file
    4. Authorise Google colab with Github
    5. Click "Ok" when prompted with a "Notebook not found" error message
    6. Open the file 
    7. Click on File -> Save a copy in Drive
    8. Click on File -> Locate in Drive
    9. Upload the "DST(Time-Series Format).csv" to the folder
    10. Open the copy of the Colab file
    11. Run the first cell and wait for the Runtime to initialise
    12. When that is finished run the rest of the cells in order
    13. Permit access to Drive when prompted


# Code Summary
1. Import the DST Index data from a CSV file and preprocess it.
2. Plot the data to visualize it.
3. Build a machine learning model using LSTM, CNN and GRU neural networks.
4. Train the model and evaluate its performance.
5. Optimise the model and compare it to other ANN models

# Conclusion and Results
This code was used for research into discovering the most accurate ANN model for predicting the DST Index. The experimentation and optimisations resulted in the 1D CNN having the lowest RMSE value and therefore the highest accuracy. A full version of the results is in the "Model Analysis.xlsx" file. 

# Future Improvements
1. Creating variable learning rate models
2. Implementing multivariate models
3. Providing a comparison to other ML and statistical models
4. Forecasting multiple data points ahead

# Acknowledgments
The DST Index data is taken from the OMNIweb website, which provides solar and space environmental data.
