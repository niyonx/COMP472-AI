# Character Classification

## Overview:
### Dataset:
The dataset (in [Assig1-Dataset](./Assig1-Dataset)) consists of 2 classes of black & white images of size 32x32:
+ Latin characters
+ Greek characters
Both include pre-splitted training set, validation set, and testing set.

### Instance Distribution:
The preview of the dataset and detailed distribution of both greek and latin class is presented in [InstanceDistribution.ipynb](./InstanceDistribution.ipynb)

### Notebooks:
Each notebook represents an experiment classification model with full life circle. The goal of those models is to give the best classification of the handwriting character black & white images of size 32x32.
+ [GNB.ipynb](./GNB.ipynb): Gaussian Naive Bayes Classifier with default parameters.
+ [Base-DT.ipynb](./Base-DT.ipynb): Base Decision Tree Classifier with default parameters.
+ [Best-DT.ipynb](./Best-DT.ipynb): Best Decision Tree Classifier with hyper-parameters found by performing grid search.
+ [Perceptron.ipynb](./Perceptron.ipynb): a Perceptron with default parameters.
+ [Base-MLP.ipynb](./Base-MLP.ipynb): Baseline Multi-Layered Perceptron.
+ [Best-MLP.ipynb](./Best-MLP.ipynb): Multi-Layered Perceptron with hyper-parameters found by performing grid search.

All output of models are written to folder [Output](./Output)

### Utils:
Folder [utils](./utils) contains methods that are used frequently in the notebooks (ie: process dataset, plot confusion matrix, etc)




