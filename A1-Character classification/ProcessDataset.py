import os
import pandas as pd
import numpy as np
import config


class character:
    def __init__(self, label, pixelValues):
        self.label = label
        self.pixelValues = pixelValues

    def get_label(self):
        return self.label

    def get_pixelValue(self):
        return self.pixelValues


def get_DataFromCSV(filename):
    headers = np.append(np.arange(0, 1024), 'CHARACTER')
    data = pd.read_csv(os.path.join(config.DATASET_PATH, filename))
    data.columns = headers
    return data


def countDistribution(filename):
    dataDist = get_DataFromCSV(filename)['CHARACTER'].value_counts()
    return dataDist.to_dict()
