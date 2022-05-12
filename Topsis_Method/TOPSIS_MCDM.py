# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:17:24 2022

@author: Mustafa.Kaynak
"""


import numpy as np
import math


class TOPSIS():
    def __init__(self,database):
        self.database=database
        
    def SCORE(self):
        sqrt_gecikme=math.sqrt((pow(self.database.iloc[:,0],2)).sum(axis=0))
        sqrt_fiyat=math.sqrt((pow(self.database.iloc[:,1],2)).sum(axis=0))
        normalize_gecikme=self.database.iloc[:,0]/sqrt_gecikme*0.30
        normalize_fiyat=self.database.iloc[:,1]/sqrt_fiyat*0.70
        
        positive_score=np.sqrt(pow(normalize_gecikme-min(normalize_gecikme),2)+pow(normalize_fiyat-min(normalize_fiyat),2))
        negative_score=np.sqrt(pow(normalize_gecikme-max(normalize_gecikme),2)+pow(normalize_fiyat-max(normalize_fiyat),2))
        
        result_score= round(negative_score/(positive_score+negative_score)*100,2)
        
        return result_score
    