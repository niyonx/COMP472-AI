DEFAULT_TRAIN_DATASET_PATH = 'data/covid_training.tsv'
DEFAULT_TEST_DATASET_PATH = 'data/covid_test_public.tsv'
DEFAULT_OUTPUT_PATH = 'output/'
DEFAULT_ALPHA = 0.01
NB_BOW_OV_filename = "trace_NB-BOW-OV.txt"
eval_NB_BOW_OV_filename = "eval_NB-BOW-OV.txt"
NB_BOW_FV_filename = "trace_NB-BOW-FV.txt"
eval_NB_BOW_FV_filename = "eval_NB-BOW-FV.txt"

header_name = ['tweet_id', 'text', 'q1_label']


def extract_data(data):
    # Change label from yes/no to binary 1 or 0
    data['q1_label'] = data['q1_label'].map({'yes': 1, 'no': 0})
    # Split data to x and y ([id, tweet] and label)
    x_data = data['text']
    y_data = data['q1_label']
    return data, x_data, y_data
