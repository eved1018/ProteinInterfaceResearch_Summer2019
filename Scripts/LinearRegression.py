#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.datasets import make_classification
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
import seaborn as sns
sns.set()
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
from scipy.special import expit


#linear regresion#

# df = pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final_sort.csv')
# df.isnull().any()
# dataset = df.fillna(method='ffill')
# X = dataset[['predus', 'ispred', 'dockpred']].values
# y = dataset['annotated'].values
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
# regressor = LinearRegression()
# regressor.fit(X_train, y_train)
# regressor.coef_
# y_pred = regressor.predict(X_test)
# results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
# print(results.head(50))

#logistic regresion#

df = pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final_sort.csv')
df.isnull().any()
dataset = df.fillna(method='ffill')
X = dataset[['predus', 'ispred', 'dockpred']].values
y = dataset['annotated'].values
lr = LogisticRegression()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
lr.fit(X_train, y_train)
print(lr.coef_)
print(lr.intercept_)
y_pred = lr.predict(X_test)
df = pd.DataFrame({'X': X_test[:,0], 'y': y_test})
df = df.sort_values(by='X')
lr.predict_proba(X_test)
confusion_matrix(y_test, y_pred)
print(lr.predict_proba(X_test))
df = pd.DataFrame({'X': X_test[:,0], 'y': y_test})
df = df.sort_values(by='X')
sigmoid_function = expit(df['X'] * lr.coef_[0][0] + lr.intercept_[0]).ravel()
plt.plot(df['X'], sigmoid_function)
plt.scatter(df['X'], df['y'], c=df['y'], cmap='rainbow', edgecolors='b')
plt.show()
