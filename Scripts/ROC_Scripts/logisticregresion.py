#!/usr/bin/env python

#import pandas
import pandas as pd
# from sklearn.linear_model import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']
# load dataset
df = pd.read_csv("/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_241/final_sort_noheader.csv", header=None, names=col_names)
# print(df.head())
df.isnull().any()
pima = df.fillna(method='ffill')

feature_cols = ['residue', 'predus', 'ispred', 'dockpred']
X = pima[feature_cols] # Features
y = pima.annotated # Target variable
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

# instantiate the model (using the default parameters)
logreg = LogisticRegression()

# fit the model with data
logreg.fit(X_train,y_train)

#prediction
y_pred=logreg.predict(X_test)
#output
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
# print(cnf_matrix)
# print(logreg.coef_)
# print(logreg.intercept_)

#auc
y_pred_proba = logreg.predict_proba(X_test)[::,1]
fpr, tpr, threshold = metrics.roc_curve(y_test,  y_pred_proba)
final = pd.DataFrame({"fpr": fpr, "tpr": tpr,"threshold": threshold})
print(final)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
# print(y_pred_proba)
results = pd.DataFrame({"predicted": y_pred_proba, "actaul" : y_test})
print(results)

plt.show()
print(auc)
