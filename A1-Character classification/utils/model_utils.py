import pandas as pd
import numpy as np
from utils import config
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

def calculate_PRF(y_true, y_pred):
    PRF = precision_recall_fscore_support(y_true, y_pred)
    precision = PRF[0].reshape(-1,1)
    recall = PRF[1].reshape(-1,1)
    F1 = PRF[2].reshape(-1,1)

    PRF_table = pd.DataFrame(np.concatenate((precision, recall, F1), axis=1))
    PRF_table.columns=['precision','recall','f1']
    return PRF_table

def show_confusion_matrix(estimator, X_Test, Y_Test, isGreekLetter):
    letters = config.GREEK_LETTERS if isGreekLetter else config.LATIN_LETTERS
    fig, ax = plt.subplots(figsize=(10, 10))
    plot_confusion_matrix(estimator, X_Test, Y_Test, ax=ax)
    ax.set_xticklabels(labels=letters)
    ax.set_yticklabels(labels=letters)
    plt.show()