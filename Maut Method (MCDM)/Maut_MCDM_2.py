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
        list_entropy=[]
        for i in self.database:
            #sum_columns0=sum(self.database[i])
            entropy_database[i]= (self.database[i])/sum(self.database[i])
            list_entropy.append(entropy_database[i])
            result_entropy=pd.DataFrame(list_entropy)
            result_entropy=np.transpose(result_entropy)
        return result_entropy

    def weighted_entropy(self):        
        #Step 4: Weight with entropy
        entropy_dataset= MultiCriteria.entropi(self)
        list_weighted=[]
        for i in self.database:
            entropy_dataset[i]= -(np.log(entropy_dataset[i]))*entropy_dataset[i]*1/(np.log(len(self.database)))
            list_weighted.append(entropy_dataset[i])
            result_entropy_weight=pd.DataFrame(list_weighted)
            result_entropy_weight=np.transpose(result_entropy_weight)
        return result_entropy_weight
        #step 5
        entropy_dataset= result_entropy_weight.fillna(value=0)
        normalize_values= MultiCriteria.normalize(self)
        
        list_entropy_fin=[]
        for i in self.database:
            sum_weigth0= (1-entropy_dataset[i]).sum(axis = 0, skipna = True)
            #entropy_dataset[i]= (1-entropy_dataset[i])/sum_weigth0
            #return entropy_dataset[i]
        entropy_dataset[i]= normalize_values[i]*entropy_dataset[i]
        list_entropy_fin.append(entropy_dataset[i])
        result_entropy_fin=pd.DataFrame(list_entropy_fin)
        result_entropy_fin= np.transpose(result_entropy_fin)
        result_entropy_fin= result_entropy_fin.fillna(value=0)
        return result_entropy_fin

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
    

    
