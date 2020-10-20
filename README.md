# Artificial Intelligence - COMP472
URL of the project: https://github.com/niyonx/COMP472-AI

# Set up the project:
## Online:

The notebooks can be previewed directly on GitHub without installing any additional software.

## Locally:
**Note:** Python 3.9 is not recommended since it is reported to have error when building `scipy` library. 
+ Recommend python version: `3.6+`
+ Full list of dependencies can be found at `requirements.txt`

### Install dependencies
+ Create virtual environment and install dependencies with the following command:
```
virtualenv --python=/usr/bin/python3.8 venv
source venv/bin/activate
pip install -r requirements.txt
```

+ Or install using [pipenv](https://pypi.org/project/pipenv/). Inside the directory, run:

```
pipenv install
```

### Start Jupyter Notebooks:
+ Using [Anaconda](https://www.anaconda.com/)
+ Using [VSCode Python Extension](https://github.com/microsoft/vscode-python). If using this method, make sure the Python interpreter path is the virtual `venv`

