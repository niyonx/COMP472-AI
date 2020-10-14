import os
import pandas as pd
import numpy as np
from utils import config
from sklearn.metrics import precision_recall_fscore_support


class character:
    def __init__(self, label, pixelValues):
        self.label = label
        self.pixelValues = pixelValues

    def get_label(self):
        return self.label

    def get_pixelValue(self):
        return self.pixelValues


def get_DataFromCSV(filename):
    data = pd.read_csv(os.path.join(config.DATASET_PATH, filename))
    if(data.shape[1] == 1025):
        headers = np.append(np.arange(0, 1024), 'CHARACTER')
    else:
        headers = np.arange(0,1024)
    data.columns = headers
    return data


def countDistribution(filename):
    dataDist = get_DataFromCSV(filename)['CHARACTER'].value_counts()
    return dataDist.to_dict()

def calculate_PRF(y_true, y_pred):
    PRF = precision_recall_fscore_support(y_true, y_pred)
    precision = PRF[0].reshape(-1,1)
    recall = PRF[1].reshape(-1,1)
    F1 = PRF[2].reshape(-1,1)

    PRF_table = pd.DataFrame(np.concatenate((precision, recall, F1), axis=1))
    PRF_table.columns=['precision','recall','f1']
    return PRF_table