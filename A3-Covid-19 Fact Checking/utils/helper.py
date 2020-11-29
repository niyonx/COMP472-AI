from sklearn.feature_extraction.text import CountVectorizer


def get_vocabulary(data, filtered=False):
    '''
    :param data: data to count words from
    :param filtered: filter out words appearing once only
    :return: count of words
    '''
    min_df = 1
    if (filtered):
        min_df = 2
    vect = CountVectorizer(min_df=min_df, lowercase=True)
    vocab = vect.fit_transform(data["text"])
    return vocab, len(vect.vocabulary_)