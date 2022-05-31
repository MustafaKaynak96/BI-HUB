# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:03:22 2022

@author: Mustafa.Kaynak
"""

import pyodbc
import pandas as pd


'''************** 1.Step is connection with MSSQL database code *********************'''
server = '.' 
database = 'LOGO_218' 
username = 'sa' 
password = 'logo'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
query = "SELECT * FROM dbo.PURCHASING_DATASET;"
df = pd.read_sql(query, cnxn)
#df['TEDARIKCI_HESAP_UNVANI']=df['TEDARIKCI_HESAP_UNVANI'].index
database=df[['ODEME_PLANI_KODU', 'MIKTAR',
'NET_ALIM_MIKTARI', 'BIRIM_FIYAT', 'KDV_ORANI', 'KDV', 'TUTAR',
'INDIRIM', 'NET_ALIM_TUTARI']]


'''************** 2.Step: Processing coming data table with Maut_MCDM library code *********************'''
from maut import MultiCriteria
maut=MultiCriteria(database)
weigh=maut.weighted_entropy()
weigh = weigh.rename_axis('Name').reset_index()
weigh = weigh.rename(columns={weigh.columns[1]: 'weighted_value'})
print(weigh.columns)
df['score']=maut.score()


'''************** 3.Step: Export result that was proccesed data to MSSQL as a created table  *********************'''
server = '.' 
database = 'BI' 
username = 'sa' 
password = 'logo'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

''' Use only one times then take in the comment row '''

cursor.execute('''
		CREATE TABLE maut_values(
			TARIH datetime,
            TEDARIKCI_HESAP_KODU text,
            TEDARIKCI_HESAP_UNVANI nvarchar(max),
            MALZEME_KODU text,
            MALZEME_ACIKLAMASI text,
            ODEME_PLANI_KODU int,
            MIKTAR float,
            NET_ALIM_MIKTARI float,
            BIRIM_FIYAT float,
            KDV_ORANI float,
            KDV float,
            TUTAR float,
            INDIRIM float,
            PROMOSYON float,
            NET_ALIM_TUTARI float,
            FIYAT_FARKI_MALIYETI float,
            score float
			)
               ''')

cnxn.commit()

for index, row in df.iterrows():
     cursor.execute("INSERT INTO maut_values (TARIH,TEDARIKCI_HESAP_KODU,TEDARIKCI_HESAP_UNVANI,MALZEME_KODU,MALZEME_ACIKLAMASI,ODEME_PLANI_KODU,MIKTAR,NET_ALIM_MIKTARI,BIRIM_FIYAT,KDV_ORANI,KDV,TUTAR,INDIRIM,NET_ALIM_TUTARI,FIYAT_FARKI_MALIYETI,score) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row.TARIH,row.TEDARIKCI_HESAP_KODU,row.TEDARIKCI_HESAP_UNVANI,row.MALZEME_KODU,row.MALZEME_ACIKLAMASI,row.ODEME_PLANI_KODU,row.MIKTAR,row.NET_ALIM_MIKTARI,row.BIRIM_FIYAT,row.KDV_ORANI,row.KDV,row.TUTAR,row.INDIRIM,row.NET_ALIM_TUTARI,row.FIYAT_FARKI_MALIYETI,row.score)
cnxn.commit()


''' Use only one times then take in the comment row'''
cursor.execute('''
		CREATE TABLE maut_weighted(
			Name text,         
            weighted_value float
			)
               ''')

cnxn.commit()

for index, row in weigh.iterrows():
     cursor.execute("INSERT INTO maut_weighted (Name,weighted_value) values(?,?)",row.Name,row.weighted_value)
cnxn.commit()
cursor.close()
    
