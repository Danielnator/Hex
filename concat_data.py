# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:31:38 2021

@author: rumin
"""

import pandas as pd


dataset = pd.read_csv("training_data/dataset_1.csv")

dataset = dataset.iloc[:, 2:]

print(dataset)

#dataset.to_csv("test.csv")

l = [dataset]

for i in range(41,146):
    d = pd.read_csv("training_data/data_" + str(i) + ".csv")
    d = d.iloc[:,1:]
    l.append(d)
    
    #print(d)
    

dataset = pd.concat(l)


dataset.to_csv("training_data/full_data.csv")


dataset = pd.read_csv("training_data/full_data.csv")

print(dataset.shape)

X = dataset.iloc[:, 1:-1].values

print(X.shape)