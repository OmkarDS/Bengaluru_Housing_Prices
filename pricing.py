#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 12:14:40 2019

@author: omkar
"""

import pandas as pd
import re

df = pd.read_csv("Predicting-House-Prices-In-Bengaluru-Train-Data.csv")

'''Cleaning total_sqft column'''

subtract_pattern = re.compile('(\d*)\s\-\s(\d*)')
yard_pattern = re.compile('(\d*)Sq. Yards')
meter_pattern = re.compile('(\d*)Sq. Meter')
acre_pattern = re.compile('(\d*)Acres')
perch_pattern = re.compile('(\d*)Perch')
int_pattern = re.compile('(\d*)\.\d*')

df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(yard_pattern, row)==None
  else str(int(re.match(yard_pattern, row).group(1)) * 9))

df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(meter_pattern, row)==None
  else str(int(re.match(meter_pattern, row).group(1)) * 10.7639))

df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(perch_pattern, row)==None
  else str(int(re.match(perch_pattern, row).group(1)) * 272.25))

df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(acre_pattern, row)==None
  else str(int(re.match(acre_pattern, row).group(1)) * 43560))

df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(subtract_pattern, row)== None 
  else str((int(re.match(subtract_pattern, row).group(1)) + int(re.match(subtract_pattern, row).group(2)))//2))

df['total_sqft'] = df['total_sqft'].apply(lambda row : row if re.match(int_pattern, row)==None
  else int(re.match(int_pattern, row).group(1)))


'''Cleaning size column'''
#size_pattern = re.compile('\d')
#size = df['size'].apply(lambda row : row if re.match(size_pattern, row)==None else int(re.match(size_pattern, row).group(0)))

df['size'] = pd.to_numeric(df['size'].str[0], errors = 'coerce')
df['size'] = df['size'].fillna(df['size'].median())

