#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:46:27 2019

@author: omkar
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import re
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.decomposition import PCA
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def cleaning(file_name,train=True):
    df = pd.read_csv(file_name)
    
    '''Cleaning total_sqft column'''
    
    subtract_pattern = re.compile('(\d*)\s\-\s(\d*)')
    yard_pattern = re.compile('(\d*)Sq. Yards')
    meter_pattern = re.compile('(\d*)Sq. Meter')
    acre_pattern = re.compile('(\d*)Acres')
    perch_pattern = re.compile('(\d*)Perch')
    cent_pattern = re.compile('(\d*)Cents')
    guntha_pattern = re.compile('(\d*)Guntha')
    ground_pattern = re.compile('(\d*)Grounds')
    float_pattern = re.compile('(\d*)\.\d*')
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(yard_pattern, row)==None
      else str(float(re.match(yard_pattern, row).group(1)) * 9))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(meter_pattern, row)==None
      else str(float(re.match(meter_pattern, row).group(1)) * 10.7639))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(perch_pattern, row)==None
      else str(float(re.match(perch_pattern, row).group(1)) * 272.25))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(acre_pattern, row)==None
      else str(float(re.match(acre_pattern, row).group(1)) * 43560))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(cent_pattern, row)==None
      else str(float(re.match(cent_pattern, row).group(1)) * 435.6))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(guntha_pattern, row)==None
      else str(float(re.match(guntha_pattern, row).group(1)) * 1089.08))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(ground_pattern, row)==None
      else str(float(re.match(ground_pattern, row).group(1)) * 2400))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(subtract_pattern, row)== None 
      else str((float(re.match(subtract_pattern, row).group(1)) + float(re.match(subtract_pattern, row).group(2)))//2))
    
    df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(float_pattern, row)==None
      else float(re.match(float_pattern, row).group(1)))
    
    df['total_sqft'] = pd.to_numeric(df['total_sqft'])
    
    
    '''Cleaning size column'''
    #size_pattern = re.compile('\d')
    #size = df['size'].apply(lambda row : row if re.match(size_pattern, row)==None 
    #   else float(re.match(size_pattern, row).group(0)))
    
    df['size'] = pd.to_numeric(df['size'].str[0], errors = 'coerce')
    df['size'] = df['size'].fillna(df['size'].median())
    
    
    '''Cleaning bath column '''
    df['bath'] = df['bath'].fillna(df['bath'].median())
    
    
    '''Cleaning balcony column '''
    df['balcony'] = df['balcony'].fillna(df['balcony'].median())
    
    
    ''' Cleaning location column '''
    df['location'] = df['location'].fillna('Whitefield')
    le_loc = LabelEncoder()
    df['location'] = le_loc.fit_transform(df['location'])
    
    
    ''' Cleaning area_type column'''
    le_area = LabelEncoder()
    df['area_type'] = le_area.fit_transform(df['area_type'])
    
    
    ''' Cleaning availability column '''
    df['availability'] = df['availability'].apply(lambda row : 
        1 if row == 'Ready To Move' else 0)
        
    
    ''' Droping columns '''
    df = df.drop(['society'], axis =1)
    if train:
        ''' Preparing X and y '''
        X_df = df.iloc[:,:-1]
        names = X_df.columns
        X = X_df.values
        y = df.iloc[:,-1].values
        
        ''' Train test split '''
        X_train, X_test, y_train, y_test = train_test_split(X, y ,test_size=0.2)
        return df,X_train, X_test, y_train, y_test, X, y
    else:
        X = df.iloc[:,:-1].values
        return df, X