import os
import pandas as pd
import numpy as np
from utils import config
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

def get_DataFromCSV(filename):
    data = pd.read_csv(os.path.join(config.DATASET_PATH, filename))
    if(data.shape[1] == 1025):
        headers = np.append(np.arange(0, 1024), 'CHARACTER')
    else:
        headers = np.arange(0,1024)
    data.columns = headers
    return data

def get_TextDataFromCSV(filename):
    return np.loadtxt(os.path.join(config.DATASET_PATH, filename), dtype=np.int, delimiter=',', skiprows=1)

def countDistribution(filename):
    dataDist = get_DataFromCSV(filename)['CHARACTER'].value_counts()
    return dataDist.to_dict()

"""
The data consists of 1025 columns, 1024 columns for each pixel and
1 row specifying the character it represents.
"""
def get_Latin_Train_Val():
    Latin_Train = np.array(get_DataFromCSV(config.LATIN_TRAIN_SET))
    Latin_X_Train = Latin_Train[:,0:1024]
    Latin_Y_Train = Latin_Train[:,1024]
    Latin_Val = np.array(get_DataFromCSV(config.LATIN_DATA_VAL))
    Latin_X_Val = Latin_Val[:,0:1024]
    Latin_Y_Val = Latin_Val[:,1024]
    return Latin_X_Train, Latin_Y_Train, Latin_X_Val, Latin_Y_Val

def get_Greek_Train_Val():
    Greek_Train = np.array(get_DataFromCSV(config.GREEK_TRAIN_SET))
    Greek_X_Train = Greek_Train[:,0:1024]
    Greek_Y_Train = Greek_Train[:,1024]
    Greek_Val = np.array(get_DataFromCSV(config.GREEK_DATA_VAL))
    Greek_X_Val = Greek_Val[:,0:1024]
    Greek_Y_Val = Greek_Val[:,1024]
    return Greek_X_Train, Greek_Y_Train, Greek_X_Val, Greek_Y_Val