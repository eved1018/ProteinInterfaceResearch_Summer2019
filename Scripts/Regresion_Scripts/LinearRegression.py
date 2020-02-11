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
import numpy as np
import statsmodels.api as sm


#linear regresion#
#
# df = pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/ROC_3/final_sort.csv')
# df.isnull().any()
# dataset = df.fillna(method='ffill')
# X = dataset[['predus', 'ispred', 'dockpred']].values
# y = dataset['annotated'].values
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
# regressor = LinearRegression()
# regressor.fit(X_train, y_train)
# coef = regressor.coef_
# y_pred = regressor.predict(X_test)
# results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
# print(results.head(50))
# print(coef)


#logistic regresion
col_names = ['residue', 'predus', 'ispred', 'dockpred', 'annotated']

df = pd.read_csv('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/noxdata.csv',header=None, names=col_names)
df.isnull().any()
dataset = df.fillna(method='ffill')
protein = dataset['residue'].values
X = dataset[['predus', 'ispred', 'dockpred']].values
y = dataset['annotated'].values
lr = LogisticRegression()
# X_train, X_test, y_train, y_test = train_test_split(X, y)
# print(y_train)
lr.fit(X, y)
print(lr.coef_)
print(lr.intercept_)
# y_pred = lr.predict(X)
# print(confusion_matrix(y, y_pred))
y_pred_proba = lr.predict_proba(X)[::,0]
# print(y_pred)
print(y_pred_proba)
# results = pd.DataFrame({"predicted": y_pred_proba, "annotated": y_test})
# path = "/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/data_241.txt"
# results.to_csv(path,sep=",", index=False, header=True)

import statsmodels.api as sm

x_train = sm.add_constant(X)
lm_1 = sm.OLS(y, x_train).fit()
print(lm_1.summary())
# logit_model=sm.Logit(X,Y)
# result=logit_model.fit()
#
# print(result.summary2())
#
# f = open('/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/regresiondata.txt', 'w')
# print(result.summary2(), file = f)


# df = pd.DataFrame({'x': X_test[:,0], 'y': y_test})
# df = df.sort_values(by='x')
# from scipy.special import expit
# sigmoid_function = expit(df['x'] * lr.coef_[0][0] + lr.intercept_[0]).ravel()
# plt.plot(df['x'], sigmoid_function)
# plt.scatter(df['x'], df['y'], c=df['y'], cmap='rainbow', edgecolors='b')
# plt.show()
