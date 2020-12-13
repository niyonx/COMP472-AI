import pandas as pd
import numpy as np
import math
from collections import Counter
import re
import string


class MultinomialNB(object):
    filter_pattern = re.compile(r'[\W_]+')

    def __init__(self, alpha, filtered, lookup_table={}):
        self.alpha = alpha
        self.filtered = filtered

    def fit(self, train_data, X, Y):
        """
        Fit the model based on train_data
        X: tweet text
        Y: label of tweet (1 or 0)
        """
        self.set_prior(Y)

        # Split the data to 2 categories
        yes_tweet = train_data[train_data['q1_label'] == 1]
        no_tweet = train_data[train_data['q1_label'] == 0]

        # Extract the vocabulary from data
        yes_vocab, yes_num_of_words = self.get_vocabulary(yes_tweet)
        no_vocab, no_num_of_words = self.get_vocabulary(no_tweet)

        # Create a full vocab from the dataset
        full_vocab = self.create_full_vocab(yes_vocab, no_vocab)
        size_of_vocab = len(full_vocab)

        # Fill up each vocab with missing words from the full_vocab
        yes_vocab = self.fill_vocab(yes_vocab, full_vocab)
        no_vocab = self.fill_vocab(no_vocab, full_vocab)

        # Create 2 lookup table for the 2 classes
        self.yes_lookup = self.generate_lookup_table(
            yes_vocab, yes_num_of_words, size_of_vocab)
        self.no_lookup = self.generate_lookup_table(
            no_vocab, no_num_of_words, size_of_vocab)
        return self

    def fill_vocab(self, vocab, full_vocab):
        """
        Fill the current vocab with words from the full_vocab
        ie: "covid" doesn't exist in yes_vocab but existed in full_vocab
        => create an entry in yes_vocab with "covid": 0
        return: the updated vocab
        """
        for word in full_vocab:
            if word not in vocab:
                vocab[word] = 0

        return vocab

    def create_full_vocab(self, yes_vocab, no_vocab):
        """
        Create a Set of vocab from both yes and no vocab (no duplicates)
        return: the set of vocab
        """
        vocab = set(yes_vocab.keys())
        vocab.update(set(no_vocab.keys()))
        return vocab

    def generate_lookup_table(self, vocab, number_of_word, size_of_vocab):
        """
        Generate a lookup table for the given vocabulary
        return: a dictionary of type ("word": probability), ie: ("covid": 0.34)
        """
        for word, frequency in vocab.items():
            # probability = (frequency + alpha) / (total-number-of-words-in-class + alpha * size of vocab)
            vocab[word] = (frequency + self.alpha) / \
                (number_of_word + self.alpha * size_of_vocab)
        return vocab

    def get_vocabulary(self, data):
        """
        Get the vocabulary given the data
        return: 
            + a dictionary in format ("word": frequency), ie: ("covid": 30)
            + length: total number of words extracted from the data (duplication counted)
        """
        min_frequency = 1
        if(self.filtered):
            min_frequency = 2
        vocab = []
        length = 0
        for index, row in data.iterrows():
            sentence_vocab, sentence_word_length = self.get_words_from_sentence(
                row['text'], ' ')
            vocab += sentence_vocab
            length += sentence_word_length

        # Counter transforms the list to a non-duplicate dict with the frequency is the value https://pymotw.com/2/collections/counter.html
        vocab = Counter(vocab)
        for word in list(vocab):
            if vocab[word] < min_frequency:
                length -= vocab[word]
                vocab.pop(word)

        return dict(vocab), length

    def get_words_from_sentence(self, line, separator):
        # split words from a sentence with the given separator (default is " ")
        words = []
        length = 0
        for each_word in line.split(separator):
            # Make word lowercase then filter out hashtags and special characters
            word = self.filter_pattern.sub('', each_word.lower())
            if (word != ''):
                words.append(word)
                length += 1
        return words, length

    def set_prior(self, Y):
        """
        Calculate the prior probability: P('yes') and P('no')
        """
        self.prior = dict()
        self.prior['p_yes'] = Y.value_counts()[1] / len(Y)
        self.prior['p_no'] = Y.value_counts()[0] / len(Y)

    def predict_line(self, line_text):
        # Give prediction from a line of text
        score_yes = self.calculate_score(line_text, 'yes')
        score_no = self.calculate_score(line_text, 'no')
        max_score = score_yes if score_yes > score_no else score_no
        prediction = 1 if score_yes > score_no else 0
        return (prediction, max_score)

    def predict(self, data):
        # Give preidction from a list of text, output is a list of predictions
        result = []
        for row in data:
            prediction, score = self.predict_line(row)
            result.append(prediction)
        return result

    def calculate_score(self, line_text, category):
        """
        Calculate the probability of a line text for the given category
        ie: calculate_score(line_text, "yes") -> score(yes) for the text
        """
        lookup_table = self.yes_lookup if category == 'yes' else self.no_lookup
        p_prior = self.prior['p_' + category]
        score = math.log10(p_prior)
        words, _ = self.get_words_from_sentence(line_text, ' ')
        # For each word, check the lookup table of that category to get the P(word | category)
        for word in words:
            if word in lookup_table:
                score += math.log10(lookup_table[word])
        return score
