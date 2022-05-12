# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:18:45 2022
@author: Mustafa.Kaynak
"""

import pyodbc
import pandas as pd
import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas.tseries.offsets import DateOffset


'''************** 1.Aşama SQL sorgusun çağırılmasısıdır. Tedarikçi seçimi için *********************'''
server = '.' 
database = 'BUDGETDB' 
username = 'sa' 
password = 'logo'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
query = "SELECT * FROM dbo.SUPPLIER_SEL;"
df = pd.read_sql(query, cnxn)




'''************** 2.Aşama Maut Algritması kullanılır. En iyi tedarikçi tespit edilir *********************'''

df[['GECIKME','BIRIM_FIYAT']]= df[['GECIKME','BIRIM_FIYAT']]
from Maut_MCDM import MultiCriteria
maut_meth=MultiCriteria(df[['GECIKME','BIRIM_FIYAT']])
#score_df=maut_meth.score_fuc()
df[['score']]=maut_meth.score_fuc()
#df.index = df['MUSTERI_UNVANI']
#del(df['MUSTERI_UNVANI'])


'''************** 3.Aşama sonuç insert into ile sql e aktarılır. *********************'''
server = '.' 
database = 'BI' 
username = 'sa' 
password = 'logo'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


''' Bir kere kullan ve ardından yorum satırına al '''

"""
cursor.execute('''
		CREATE table Supplier_table (
			Supplier_name nvarchar(500),
            Product_name nvarchar(500),
            Product_cod nvarchar(500),
			Unit_price float,
            Delay_time int,
            score float
			)
               ''')
cnxn.commit()
"""

#print(df.columns)


for index, row in df.iterrows():
     cursor.execute("INSERT INTO Supplier_table (Supplier_name,Product_name,Product_cod,Unit_price,Delay_time,score) values(?,?,?,?,?,?)", row.MUSTERI_UNVANI, row.MALZEME_KODU, row.MALZEME_ADI, row.BIRIM_FIYAT, row.GECIKME, row.score)
cnxn.commit()
cursor.close()
