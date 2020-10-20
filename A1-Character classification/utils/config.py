import os
import pandas as pd


def create_DictOfInfo(infoPath):
    info = pd.read_csv(infoPath)
    info = info.transpose()
    return info.to_dict(orient='records')[1]


DATASET_PATH = './Assig1-Dataset'
OUTPUT_PATH = './Output'

LATIN_TRAIN_SET = 'train_1.csv'
LATIN_INFO = 'info_1.csv'
LATIN_DATA_VAL = 'val_1.csv'
LATIN_TEST_NOLABEL = 'test_no_label_1.csv'
LATIN_TEST_LABEL = 'test_with_label_1.csv'
LATIN_INFO_DICT = create_DictOfInfo(os.path.join(DATASET_PATH, LATIN_INFO))
LATIN_LETTERS = list(LATIN_INFO_DICT.values())

GREEK_TRAIN_SET = 'train_2.csv'
GREEK_INFO = 'info_2.csv'
GREEK_DATA_VAL = 'val_2.csv'
GREEK_TEST_NOLABEL = 'test_no_label_2.csv'
GREEK_TEST_LABEL = 'test_with_label_2.csv'
GREEK_INFO_DICT = create_DictOfInfo(os.path.join(DATASET_PATH, GREEK_INFO))
GREEK_LETTERS = list(GREEK_INFO_DICT.values())
