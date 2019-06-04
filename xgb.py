#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:46:45 2019

@author: omkar
"""

from cleaning import cleaning

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import re
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.decomposition import PCA
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

file_name = 'Predicting-House-Prices-In-Bengaluru-Train-Data.csv'
df, X_train, X_test, y_train, y_test,X,y = cleaning(file_name)

#corr = df.corr()
#
#scaler = StandardScaler()
#df.iloc[:,:-1] = scaler.fit_transform(df.iloc[:,:-1])

''' Model '''
regressor = xgb.XGBRegressor()

#''' GridsearchCV '''
#parameters = {'gamma' : [0.01], 'learning_rate': [0.08],
#              'n_estimators':[51], 'subsample' : [1],
#              'colsample_bytree' : [1], 'max_depth' : [4]}
#gs = GridSearchCV(regressor, parameters)
#gs.fit(X_train,y_train)
#
#best_score = gs.best_score_
#best_params = gs.best_params_

regressor = xgb.XGBRegressor(gamma=0.01,learning_rate=0.08,
                             n_estimators=51,subsample=1,
                             colsample_bytree=1,max_depth=4
                            )

cv_results = cross_val_score(regressor,X,y,cv=5)

regressor.fit(X_train, y_train)
train_predictions = regressor.predict(X_train)

predictions = regressor.predict(X_test)
#print(regressor.score(X_test, y_test))



#''' Performance '''
#rmse_train = np.sqrt(mean_squared_error(y_train, train_predictions))
#print("RMSE train: %f" % (rmse_train))
#
#rmse = np.sqrt(mean_squared_error(y_test, predictions))
#print("RMSE test: %f" % (rmse))

def rmsle(y_pred,y_test) :
    error = np.square(np.log10(y_pred +1) - np.log10(y_test +1)).mean() ** 0.5
    Acc = 1 - error
    return Acc

print(rmsle(train_predictions, y_train))
print(rmsle(predictions, y_test))

#test_file = 'Predicting-House-Prices-In-Bengaluru-Test-Data.csv'
#test_df, test_X = cleaning(test_file, train=False)
#
#final_prediction = regressor.predict(test_X)
#final_prediction = pd.DataFrame(final_prediction,columns = ['price'],index=None)
#final_prediction.to_excel("results.xlsx",index=False)

