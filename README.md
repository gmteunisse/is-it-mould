# Is it mould?
## Introduction
This repository is an exploration of mould on kombucha pellicles. In this project, (1) we will create a kombucha mould data set, (2) train and validate a classifier and (3) deploy a web app for future predictions.

## Set up
This entire project will be written in Python. To avoid dependency errors, we will make use of Anaconda (`conda`) environments. You can install `conda` using the instructions on [this page](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). We recommend installing Miniconda, but feel free to go for the full installation of Anaconda.

After installing `conda`, make sure to install the Python Reddit API Wrapper (praw) environment:

```
conda install -c conda-forge praw
```

## Creating a Reddit application
We will be scraping the `r/kombucha` subreddit for this project. This requires setting up a Reddit application. Head over to [the authorized applications page](https://www.reddit.com/prefs/apps) and create a new script at the bottom. It is required to add a redirect uri, use `http://localhost:8080` here. Once your apps has been created, you will have the required credentials to start using the Reddit API.