import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

import data_splitting
import data_sampling
import submission_file

#DATA READING

account = pd.read_csv('../data/account.csv',delimiter=";")
card_train = pd.read_csv('../data/card_train.csv',delimiter=";")
client = pd.read_csv('../data/client.csv',delimiter=";")
disp = pd.read_csv('../data/disp.csv',delimiter=";")
district = pd.read_csv('../data/district.csv',delimiter=";")
loan_train = pd.read_csv('../data/loan_train.csv',delimiter=";")

competition = pd.read_csv('../data/loan_test.csv',delimiter=";")

#trans_train = pd.read_csv('../data/trans_train.csv',delimiter=";")

#DATA JOINING


#DATA CLEANING


#DATA SPLITTING

split_data = data_splitting.split(loan_train)

train = split_data[0]
test = split_data[1]

#DATA SAMPLING

train = data_sampling.sampling(train)

#MODEL BUILDING

# Preparing data for classifier
training_inputs = train[['date', 'amount',
                         'duration', 'payments']].values

training_labels = train['status'].values


testing_inputs = test[['date', 'amount',
                         'duration', 'payments']].values

testing_labels = test['status'].values


from sklearn.tree import DecisionTreeClassifier

# Create the classifier
decision_tree_classifier = DecisionTreeClassifier()

# Train the classifier on the training set
decision_tree_classifier.fit(training_inputs, training_labels)

# Validate the classifier on the testing set using classification accuracy
score = decision_tree_classifier.score(testing_inputs, testing_labels)
print("Not sure what score: {}".format(score))

predicted = decision_tree_classifier.predict(testing_inputs)
print("AUC score: {}".format(roc_auc_score(testing_labels, predicted)))

#MODEL APPLYING AND OBTAINING PREDICTION

submission_file.create(competition,decision_tree_classifier)







