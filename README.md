# Is it mould?
## Introduction
This repository is an exploration of mould on kombucha pellicles. In this project, (1) we will create a kombucha mould data set by scraping reddit and storing the results in a SQL database, (2) train and validate a classifier and (3) deploy a web app and/or reddit bot for future predictions.

## Set up
### Conda
This entire project will be written in Python. To avoid dependency errors, we will make use of Anaconda (`conda`) environments. You can install `conda` using the instructions on [this page](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). We recommend installing Miniconda, but feel free to go for the full installation of Anaconda.

# PRAW
After installing `conda`, make sure to install the Python Reddit API Wrapper (`praw`) in a new environment. This environment contains a python 3.x distribution and the `praw` python library, as well as all libraries required to run `praw`.

```
# Install PRAW, required for scraping
conda create -n praw -c conda-forge praw

# Install PSAW, only required as part of `test_scraping.ipynb`
conda activate praw
pip3 install psaw
conda deactivate
```

## Creating a Reddit application
We will be scraping the `r/kombucha` subreddit for this project. This requires setting up a Reddit application. Head over to [the authorized applications page](https://www.reddit.com/prefs/apps) and create a new script at the bottom. It is required to add a title, description and redirect uri (use `http://localhost:8080` here). Once your apps has been created, you will have the required credentials to start using the Reddit API.