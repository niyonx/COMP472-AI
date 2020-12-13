# Covid-19 Tweet Fact Checking

URL: https://github.com/niyonx/COMP472-AI/tree/main/A3-Covid-19%20Fact%20Checking

## Structure

```
A3-Covid-19\ Fact\ Checking
├── Handout.pdf
├── NB_BOW.py
├── READM.md
├── data
│   ├── covid_test_public.tsv
│   └── covid_training.tsv
├── main.py
├── output
│   ├── eval_LSTM.txt
│   ├── eval_NB-BOW-FV.txt
│   ├── eval_NB-BOW-OV.txt
│   ├── trace_LSTM.txt
│   ├── trace_NB-BOW-FV.txt
│   └── trace_NB-BOW-OV.txt
└── utils.py

2 directories, 13 files
```

- `NB_BOW.py`: the class of Naive Bayes Bag-of-Word model. The class has

  - `fit()` function, used to train model.
  - `predict_line()` to classify if a line of tweet contains COVID-19 facts.
  - `predict()` takes a list of tweet data and classify each tweet

- `main.py`: Contains functions to process data, then train and test model.

- `output`: The output files, containing trace file and eval file of the model after running through test data.

## Run

- `python3 main.py` to train model and predict from test file.
