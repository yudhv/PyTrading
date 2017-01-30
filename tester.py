import pandas as pd
from getter import download_data

def result(df):
	kurt = kurtosis(df)
	mn = mean(df)
	# if(kurt <=0):
	# 	return ((mn*12.5)**1.5)*(abs(kurt)+1)
	# else: return (mn*12.5)**1.5/kurt
	vol = df['VOLUME'].mean()
	cls = df['CLOSE'].mean()
	# return vol/(cls*mn)
	return vol*cls

def change_adder(df):
	# df['Percent Change'] = (df.ix[:,'HIGH']/df.ix[:,'LOW']-1)*100
	df1=df.copy()
	df1[1:] = abs(df[1:]/df[0:-1].values-1)*100
	df1.ix[0:10,:]=0
	df['Percent Change'] = df1['CLOSE']
	
	return df

def make_list():
	kurt=pd.DataFrame(
		{'SYMBOL':'hello',
		'MEAN CHANGE':0.0,
		'KURTOSIS':0.0,
		'RESULT':0.0},index=[0])
	#print kurt.dtypes
	kurt = kurt[['SYMBOL',
		'MEAN CHANGE',
		'KURTOSIS',
		'RESULT']]
	return kurt

def append_list(df,symbol,kurti):
	row = pd.Series([symbol,mean(df),kurtosis(df),result(df)],
		index=['SYMBOL','MEAN CHANGE','KURTOSIS','RESULT'])
	kurti = kurti.append(row,ignore_index=True)
	return kurti

def sort_list(df):
	df = df.sort_values(by='RESULT',ascending=False)
	df = df.reset_index(drop=True)
	df = df.drop(df.tail(1).index)
	if(len(df)>150): df=df.ix[0:150]
	return df

def calculate_result(sym,days):
	mn = 0
	kurt = 0
	res = 0
	start = 1
	end = days +1
	
	for i in range(start,end):
		df = download_data(sym,i)
		df = change_adder(df)
		mn += mean(df)
		kurt += kurtosis(df)
		res += result(df)
	res /= days
	mn /= days
	kurt /= days
	return res,mn,kurt

def mean(df):
	return df['Percent Change'].mean()

def kurtosis(df):
	return df['Percent Change'].kurtosis()

def rejectable(df):
	# if(len(df)<300): return True
	if(df['CLOSE'].mean()>=56): return True
	if(df['CLOSE'].mean()*df['VOLUME'].median()<10000): return True
