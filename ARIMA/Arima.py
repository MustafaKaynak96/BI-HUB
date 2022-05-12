# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 22:29:17 2022

@author: Mustafa.Kaynak
"""

import pyodbc
import pandas as pd
import itertools
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas.tseries.offsets import DateOffset

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '.' 
database = 'LOGO_218' 
username = 'sa' 
password = 'logo'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT * FROM dbo.SATIS_FOR_PREDICT;"
df = pd.read_sql(query, cnxn)

df=df.sort_values(by=['TARIH'],ascending=True)
df.index = pd.to_datetime(df['TARIH'])
del(df['TARIH'])
df = df['NET_SATIS_TUTARI'].groupby(df.index).sum()


Q1=np.quantile(df,0.35)
Q3=np.quantile(df,0.75)
IQR= Q3-Q1
upper_outlier= Q3+ 1.5*IQR
lower_outlier= Q1- 1.5*IQR
#df1=df[(df>upper_outlier) | (df<lower_outlier)]
#df1=df1.mean()
#df1=df1.astype(int)

df=df.ffill()
df.plot()
plt.legend()
plt.show()



y = df
print(y)

y.plot(figsize=(15, 6))
plt.show()

# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()

print(results.summary().tables[1])

results.plot_diagnostics(figsize=(15, 12))
plt.show()
min_date=min(y.index)
pred = results.get_prediction(start=pd.to_datetime(min_date), dynamic=False)


pred_ci = pred.conf_int()



ax = y['2011':].plot(label='Gözlemlenen')
pred.predicted_mean.plot(ax=ax, label='Tahminler', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Tarih')
ax.set_ylabel('Net Satış Tutarı')
plt.legend()

plt.show()


y_forecasted = pred.predicted_mean.astype(int)
y_truth = y[min_date:]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))


pred_dynamic = results.get_prediction(start=pd.to_datetime(min_date), dynamic=True, full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()

ax = y[min_date:].plot(label='observed', figsize=(20, 15))
pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

ax.fill_between(pred_dynamic_ci.index,
                pred_dynamic_ci.iloc[:, 0],
                pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

ax.fill_betweenx(ax.get_ylim(), pd.to_datetime(min_date), y.index[-1],
                 alpha=.1, zorder=-1)

ax.set_xlabel('Date')
ax.set_ylabel('Net Satış Tutarı')

plt.legend()
plt.show()


#y_forecasted = pred_dynamic.predicted_mean

y_truth = y[min_date:]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))


steps_size=100
pred_uc = results.get_forecast(steps=steps_size)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()
pred_ci.columns = pred_ci.columns.str.replace('lower NET_SATIS_TUTARI', 'lower')
pred_ci.columns = pred_ci.columns.str.replace('upper NET_SATIS_TUTARI', 'upper')
pred_ci_dates=[pred_dynamic_ci.index[-1]+ DateOffset(days=x)for x in range(1,steps_size+1)]
#future_datest_df=pd.DataFrame(index=future_dates,data=history)
print(pred_ci.columns)

pr_me=pred_uc.predicted_mean
pr_me.index= pd.to_datetime(pred_ci_dates)
pred_ci.index = pd.to_datetime(pred_ci_dates)

"""
pred_ci.plot()
pr_me.plot()
ax.set_xlabel('Date')
ax.set_ylabel('Net Satış Tutarı')

plt.legend()
plt.show()
"""


res=pd.concat([pr_me,pred_ci],axis=1)
res['Tarih']=res.index
res['predicted_mean']=res['predicted_mean']
res['predicted_mean_low']=res['predicted_mean']-res['predicted_mean']*0.33
res['predicted_mean_up']=res['predicted_mean']+res['predicted_mean']*0.33


#df['BD.SIRKET_ADI']=database[['BD.SIRKET_ADI']]
res.plot()
ax.set_xlabel('Date')
ax.set_ylabel('Net Satış Tutarı')

plt.legend()
plt.show()


#res.to_csv('ARIMA_RESULT.csv')
#y.to_csv('REal_data.csv')



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
		CREATE TABLE Sales_Values (
			Date datetime,
            Predict_mean int,
            Low_Sales int,
			Upper_Sales int,
            Predict_Mean_Low int,
            Predict_Mean_Up int
			)
               ''')

cnxn.commit()
"""

print(res.columns)


for index, row in res.iterrows():
     cursor.execute("INSERT INTO Sales_Values (Date,Predict_mean,Low_Sales,Upper_Sales,Predict_Mean_Low,Predict_Mean_Up) values(?,?,?,?,?,?)", row.Tarih, row.predicted_mean, row.lower, row.upper, row.predicted_mean_low, row.predicted_mean_up)
cnxn.commit()
cursor.close()


