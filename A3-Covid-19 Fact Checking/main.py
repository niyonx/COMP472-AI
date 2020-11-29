from NB_BOW import MultinomialNB
import pandas as pd
import numpy as np

# Loading data
train_data = pd.read_csv('data/covid_training.tsv', sep='\t').iloc[:, 0:3]
test_data = pd.read_csv('data/covid_test_public.tsv',
                        sep='\t',
                        names=train_data.columns.values.tolist(),
                        header=None,
                        usecols=[0, 1, 2]).iloc[:, 0:3]

# Changing target from yes/no to 1/0
train_data['q1_label'] = train_data['q1_label'].map({'yes': 1, 'no': 0})
test_data['q1_label'] = test_data['q1_label'].map({'yes': 1, 'no': 0})

# Splitting into training and testing
X_train = train_data.iloc[:, 0:2]
y_train = train_data['q1_label']
X_test = test_data.iloc[:, 0:2]
y_test = test_data['q1_label']

print("True:\n",np.array(y_test),"\n")

# NB-BOW-OV
nb = MultinomialNB(filtered=False).fit(X_train, y_train)

y_pred = np.array(nb.predict(X_test))
print("Predicted:\n",y_pred)

total = len(y_test)
val = 0
for i, j in zip(y_pred, y_test):
    if i == j:
        val += 1
    else:
        pass

print(f"Original Vocabulary Error:\t {(1-(val/total)):.1%}\n")

# NB-BOW-FV
nb = MultinomialNB(filtered=True).fit(X_train, y_train)

y_pred = np.array(nb.predict(X_test))
print("Predicted:\n",y_pred)

total = len(y_test)
val = 0
for i, j in zip(y_pred, y_test):
    if i == j:
        val += 1
    else:
        pass

print(f"Filtered Vocabulary Error:\t {(1-(val/total)):.1%}\n")