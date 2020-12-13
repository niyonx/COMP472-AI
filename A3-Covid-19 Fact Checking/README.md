## Covid-19 Fact Checking

We use a Naive Bayes bag-of-Word (NB-BOW) approach to determine if a tweet contains a verifiable factual claim or not.

The dataset is already split into a training set of 400 instances and a test set of 55 instances in the folder [data](./data/).

A preview and analysis of the dataset distributions are shown in [DatasetAnalysis.ipynb](./DatasetAnalysis.ipynb).

The file [utils.py](./utils.py) contains global variables and a method to extract data.

The NB-BOW model is in [NB_BOW.py](./NB_BOW.py) with boolean parameter filtered in the constructor to specify using the OV or the FV.

### How to run

- Run [main.py](./main.py) to run both models.
- Outputs are generated to folder [output](./output/)
