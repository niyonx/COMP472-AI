from NB_BOW import MultinomialNB
import pandas as pd
import numpy as np
import os
from utils import extract_data, header_name, DEFAULT_TRAIN_DATASET_PATH, DEFAULT_TEST_DATASET_PATH, DEFAULT_OUTPUT_PATH, DEFAULT_ALPHA, NB_BOW_OV_filename, eval_NB_BOW_OV_filename, NB_BOW_FV_filename, eval_NB_BOW_FV_filename


def train_model(train_data_path, filtered, alpha_smooth):
    # Load training dataset
    train_data = pd.read_csv(train_data_path, sep='\t').iloc[:, 0:3]
    train_data, X_train, Y_train = extract_data(train_data)
    # Train model
    return MultinomialNB(alpha_smooth, filtered).fit(train_data, X_train, Y_train)


def test_model(model, test_data_path, output_dir, output_file_name, eval_file_name):
    # Read and extract test data set
    test_data = pd.read_csv(test_data_path,
                            sep='\t',
                            names=header_name,
                            header=None,
                            usecols=[0, 1, 2]).iloc[:, 0:3]
    test_data, x_test, y_test = extract_data(test_data)
    print("Correct labels:\n", np.array(y_test), "\n")

    # Start predicting line by line and write to output file
    output_path = os.path.join(output_dir, output_file_name)
    output_file = open(output_path, "w")

    predictions = []
    num_of_correct = 0
    for index, row in test_data.iterrows():
        # Make prediction
        line_prediction, max_score = model.predict_line(row['text'])
        predictions.append(line_prediction)

        # Evaluate if the prediction is correct or not
        line_prediction = "yes" if line_prediction else "no"
        target = "yes" if row['q1_label'] else "no"
        outcome = "correct" if line_prediction == target else "wrong"

        if (outcome == 'correct'):
            num_of_correct += 1

        # Write result to file
        content = """{}  {}  {:.4}  {}  {}\n""".format(
            row['tweet_id'], line_prediction, str(max_score), target, outcome)

        output_file.write(content)

    output_file.close()
    print("Predicted labels:\n", predictions)
    print("Trace file produced: ", output_path)
    # TODO: Calculate and print out precision and stats
    evaluate(y_test.tolist(), predictions,
             os.path.join(output_dir, eval_file_name), num_of_correct)


def evaluate(y_true, y_pred, eval_file_path, num_of_correct):
    # Number of instace is put in 'yes' and should be in 'yes' (True Positive)
    TP_yes = 0
    # Number of instace is put in 'yes' but should be in 'no' (False Positive)
    FP_yes = 0
    # Number of instace is put in 'no' and should be in 'no' (True Positive)
    TP_no = 0
    # Number of instace is put in 'no' but should be in 'yes' (False Positive)
    FP_no = 0
    for each in range(len(y_true)):
        if y_true[each] and y_pred[each]:
            TP_yes += 1
        if y_true[each] == 0 and y_pred[each] == 0:
            TP_no += 1
        if y_true[each] == 0 and y_pred[each] == 1:
            FP_yes += 1
        if y_true[each] == 1 and y_pred[each] == 0:
            FP_no += 1

    acc = num_of_correct / len(y_pred)
    prec_yes = TP_yes / (TP_yes + FP_yes)
    rec_yes = TP_yes / (TP_yes + FP_no)
    prec_no = TP_no / (TP_no + FP_no)
    rec_no = TP_no / (TP_no + FP_yes)
    f1_yes = 2 * (prec_yes * rec_yes) / (prec_yes + rec_yes)
    f1_no = 2 * (prec_no * rec_no) / (prec_no + rec_no)

    eval_file = open(eval_file_path, "w")
    eval_file.write("{:.4}\n".format(acc))
    eval_file.write("{:.4}  {:.4}\n".format(prec_yes, prec_no))
    eval_file.write("{:.4}  {:.4}\n".format(rec_yes, rec_no))
    eval_file.write("{:.4}  {:.4}\n".format(f1_yes, f1_no))
    eval_file.close()
    print('Eval file produced: ', eval_file_path)


print('Original Vocabulary \n')
NB_BOW_OV_model = train_model(DEFAULT_TRAIN_DATASET_PATH, False, DEFAULT_ALPHA)
test_model(NB_BOW_OV_model, DEFAULT_TEST_DATASET_PATH,
           DEFAULT_OUTPUT_PATH, NB_BOW_OV_filename, eval_NB_BOW_OV_filename)

print('\nFiltered Vocabulary \n')
NB_BOW_FV_model = train_model(DEFAULT_TRAIN_DATASET_PATH, True, DEFAULT_ALPHA)
test_model(NB_BOW_FV_model, DEFAULT_TEST_DATASET_PATH,
           DEFAULT_OUTPUT_PATH, NB_BOW_FV_filename, eval_NB_BOW_FV_filename)
