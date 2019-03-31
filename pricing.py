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
