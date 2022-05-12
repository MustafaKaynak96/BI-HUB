# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:03:48 2022

@author: Mustafa.Kaynak
"""

import pyodbc
import pandas as pd


'''************** 1.Aşama SQL sorgusun çağırılmasısıdır. Tedarikçi seçimi için *********************'''
server = '.' 
database = 'BUDGETDB' 
username = 'sa' 
password = 'logo'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
query = "SELECT * FROM dbo.SUPPLIER_SEL;"
df = pd.read_sql(query, cnxn)

'''************** 2.Aşama MCDM Algoritması çalıştırılır. *********************'''

from TOPSIS_MCDM import TOPSIS
topsis_method= TOPSIS(df[['GECIKME','BIRIM_FIYAT']])
df['score']=topsis_method.SCORE()


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
for index, row in df.iterrows():
     cursor.execute("INSERT INTO Supplier_table (Supplier_name,Product_name,Product_cod,Unit_price,Delay_time,score) values(?,?,?,?,?,?)", row.MUSTERI_UNVANI, row.MALZEME_KODU, row.MALZEME_ADI, row.BIRIM_FIYAT, row.GECIKME, row.score)
cnxn.commit()
cursor.close()

print("program is complete . . .")
