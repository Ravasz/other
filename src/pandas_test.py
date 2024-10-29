'''
Created on 11 Mar 2018

@author: mate
'''


import pandas as pd
import numpy as np

standardsDf= pd.read_csv('/media/sf_Xubuntu/Hypothetical dataset2.csv',sep='\t') 

sample3Df= pd.read_csv('/media/sf_Xubuntu/Sample3.csv',sep='\t') 

for indexVals, rowO in sample3Df.iterrows():
  if np.isclose(rowO["PositiveMode"],standardsDf["PositiveMode"],atol = 0.02).any():
    print(rowO["Compound"])


