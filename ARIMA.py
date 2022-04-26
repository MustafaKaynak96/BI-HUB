# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 22:55:43 2022

@author: Mustafa.Kaynak
"""


import pyodbc
import pandas as pd
import itertools
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas.tseries.offsets import DateOffset

"""*****************  1.Aşama SQL tarafında var olan tabloyu python ile okumak  *************************** """

server = '.' 
database = 'BI' 
username = 'sa' 
password = 'deneme'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT * FROM dbo.SATIS_FOR_PREDICT;"
df = pd.read_sql(query, cnxn)

"""*****************  2.Aşama Dataframe ve index düzenlemeleri  *************************** """

df=df.sort_values(by=['TARIH'],ascending=True)
df.index = pd.to_datetime(df['TARIH'])
del(df['TARIH'])
df = df['NET_SATIS_TUTARI'].groupby(df.index).sum()

df=df.ffill()
df.plot()
plt.legend()
plt.show()
y = df
y.plot(figsize=(15, 6))
plt.show()



"""*****************  3.Aşama ARIMA Zaman serisi Algoritması  *************************** """
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()
#print(results.summary().tables[1])
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
mse = ((y_forecasted - y_truth) ** 2).mean()


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


y_truth = y[min_date:]
mse = ((y_forecasted - y_truth) ** 2).mean()



"""*****************  4.Aşama ARIMA Zaman serisi Algoritmasının Tahminlenmesi  *************************** """
steps_size=100
pred_uc = results.get_forecast(steps=steps_size)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()
pred_ci.columns = pred_ci.columns.str.replace('lower Net Satış Tutarı', 'lower')
pred_ci.columns = pred_ci.columns.str.replace('upper Net Satış Tutarı', 'upper')
pred_ci_dates=[pred_dynamic_ci.index[-1]+ DateOffset(days=x)for x in range(1,steps_size+1)]
#future_datest_df=pd.DataFrame(index=future_dates,data=history)

pr_me=pred_uc.predicted_mean
pr_me.index= pd.to_datetime(pred_ci_dates)
pred_ci.index = pd.to_datetime(pred_ci_dates)



"""*****************  5.Aşama Sonuçların Qlik sense kullanımı için csv olarak aktarılması  *************************** """
res=pd.concat([pr_me,pred_ci],axis=1)
res['predicted_mean']=res['predicted_mean']
res['predicted_mean_low']=res['predicted_mean']-res['predicted_mean']*0.33
res['predicted_mean_up']=res['predicted_mean']+res['predicted_mean']*0.33
res.plot()
ax.set_xlabel('Date')
ax.set_ylabel('Net Satış Tutarı')
plt.legend()
plt.show()
res.to_csv('ARIMA_RESULT.csv')






