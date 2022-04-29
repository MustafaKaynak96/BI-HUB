# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 23:50:08 2021

@author: Mustafa
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class MultiCriteria():
    def __init__(self,database):
        self.database=database
    
    def normalize(self):
        from sklearn.preprocessing import MinMaxScaler
        nrm= MinMaxScaler()
        Normalize_database=nrm.fit_transform(self.database)
        return Normalize_database
    
    def entropi(self):
        entropy_database= MultiCriteria.normalize(self)
        entropy_database= pd.DataFrame(data=self.database)
        
        for i in self.database:
            sum_columns0=sum(self.database[i])
            entropy_database[i]= (self.database[i])/sum_columns0
        return entropy_database
    
    def weighted_entropy(self):        
        #Step 4: Weight with entropy
        entropy_dataset= MultiCriteria.entropi(self)
        for i in self.database:
            entropy_dataset[i]= -(np.log(entropy_dataset[i]))*entropy_dataset[i]*1/(np.log(len(self.database)))
        return entropy_dataset
        #step 5
        entropy_dataset= entropy_dataset.fillna(value=0)
        normalize_values= MultiCriteria.normalize(self)
        
        for i in self.database:
            sum_weigth0= sum(1-entropy_dataset[i])
            entropy_dataset[i]= (1-entropy_dataset[i])/sum_weigth0
            entropy_dataset[i]= normalize_values[i]*entropy_dataset[i]
        return entropy_dataset
    
    
    def score_fuc(self):
        Normalize_database= MultiCriteria.normalize(self)
        entropy_database= MultiCriteria.weighted_entropy(self)
        for i in self.database:
            last_fg= Normalize_database*entropy_database
        #Last Score Step
        last_fg['score']= last_fg.sum(axis=1)
        result_score= pd.DataFrame(last_fg['score'])
        result_score= result_score.fillna(value=0)
        #result_score.append(last_fg)
        
        #Vizualization of result score
        plt.bar(last_fg.index,last_fg['score'])
        plt.xticks(rotation=90)
        plt.show()
        return result_score
    
