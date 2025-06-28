import pandas as pd
import numpy as np
from sklearn import preprocessing
import os

# feature engineering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# models
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression


# metrics for evaluation
from sklearn.metrics import jaccard_score
from sklearn.metrics import hamming_loss
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

# visualization libs
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


toys = pd.read_json('/kaggle/input/amazon-product-review-spam-and-non-spam/Toys_and_Games/Toys_and_Games.json', lines=True)
toys_df = toys.drop(['unixReviewTime', 'reviewerID', 'asin'], axis=1)
toys = []
toys_df = toys_df.dropna(subset=['class'])

toys_df = toys_df.rename(columns={"overall": "rating", "helpful" : "votes-down/up"})
# toys_df['reviewText'] = toys_df['reviewText'].astype('str')

# id column cleanup
toys_df = toys_df.rename(columns={"_id": "id"})
toys_df['id'] = toys_df['id'].dropna()
toys_df['id'] = toys_df['id'].astype('str')
toys_df['id'] = toys_df['id'].str.split(' ').str[1].str.replace('}', '').str[1:-1]

# review time column cleanup
toys_df['reviewTime'] = toys_df['reviewTime'].str.replace(',', '').str.replace(' ', '.')

# text columns cleanup
toys_df['reviewText'] = toys_df['reviewText'].str.lower().str.replace('[^\w\s]', '')
toys_df = toys_df.loc[toys_df['reviewText'].str.len() > 90] # average length of the sentace is 20-25 words at 4.7 chars per word hence 90 characters or below is filtered

toys_df