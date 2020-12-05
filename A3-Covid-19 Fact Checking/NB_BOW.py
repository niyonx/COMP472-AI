from utils.helper import get_vocabulary
import pandas as pd
import numpy as np


class MultinomialNB(object):
    def __init__(self, alpha=0.01, filtered=False):
        self.alpha = alpha
        self.filtered = filtered

    def fit(self, X, y):
        
        # Get Vocabulary
        X, train_vocab_length, training_vocab = get_vocabulary(X, self.filtered)

        # Calculate probability of each class
        self.prior = {}
        total = y.value_counts().sum()

        for i, cat in enumerate(y.value_counts(sort=False)):
            self.prior[i] = cat / total

        # Create word probability table
        docIdx, wordIdx = X.nonzero()
        count = X.data
        classIdx = []
        for idx in docIdx:
            classIdx.append(y[idx])

        df = pd.DataFrame()
        df["docIdx"] = np.array(docIdx)
        df["wordIdx"] = np.array(wordIdx)
        df["count"] = np.array(count)
        df["classIdx"] = np.array(classIdx)

        # Calculate probability of each word based on class
        pb_ij = df.groupby(['classIdx', 'wordIdx'])
        pb_j = df.groupby(['classIdx'])
        Pr = (pb_ij['count'].sum() + self.alpha) / (pb_j['count'].sum() +
                                                    train_vocab_length)

        # Unstack series
        Pr = Pr.unstack()

        # Replace NaN or columns with 0 as word count with alpha / (count + |V| +1)
        for c in range(0, 1):
            Pr.loc[c, :] = Pr.loc[c, :].fillna(
                self.alpha / (pb_j['count'].sum()[c] + train_vocab_length + 1))

        # Convert to dictionary for greater speed
        self.Pr_dict = Pr.to_dict()

        self.training_vocab = training_vocab

        return self

    def predict(self, X):

        # Get new document term matrix from previously learned vocabulary in training
        X = self.training_vocab.transform(X["text"])

        docIdx, wordIdx = X.nonzero()
        count = X.data

        df = pd.DataFrame()
        df["docIdx"] = np.array(docIdx)
        df["wordIdx"] = np.array(wordIdx)
        df["count"] = np.array(count)

        # Using dictionaries for greater speed
        df_dict = df.to_dict()
        new_dict = {}
        prediction = []

        # new_dict = {docIdx : {wordIdx: count},....}
        for idx in range(len(df_dict['docIdx'])):
            docIdx = df_dict['docIdx'][idx]
            wordIdx = df_dict['wordIdx'][idx]
            count = df_dict['count'][idx]
            try:
                new_dict[docIdx][wordIdx] = count
            except:
                new_dict[df_dict['docIdx'][idx]] = {}
                new_dict[docIdx][wordIdx] = count

        # Calculating the scores for each doc
        for docIdx in range(0, len(new_dict)):
            score_dict = {}
            # Creating a probability row for each class
            for classIdx in range(0, 2):
                score_dict[classIdx] = 1
                # For each word:
                for wordIdx in new_dict[docIdx]:
                    # Check for frequency smoothing
                    # log(1+f)*log(Pr(i|j))
                    try:
                        probability = self.Pr_dict[wordIdx][classIdx]
                        power = np.log10(1 + new_dict[docIdx][wordIdx])
                        score_dict[classIdx] += power * np.log10(probability)
                    except:
                        # Missing V = 0
                        score_dict[classIdx] += 0

                # Multiply final with prior
                score_dict[classIdx] += np.log10(self.prior[classIdx])

            # Get class with max probabilty for the given docIdx
            max_score = max(score_dict, key=score_dict.get)
            prediction.append(max_score)

        return prediction