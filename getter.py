import pandas as pd
import numpy as np

def download_data(quote,day=0):
	days = day+1
	url1='http://www.google.com/finance/getprices?q='
	url2='&x=NSE&i=60&p='
	url3='d&f=d,c,o,h,l,v&df=cpct&auto=1&ts=1266701290218' 
	#Not using the ts=1266701290218 parameter, if something goes wrong, do try it
	df = pd.read_csv(url1+quote+url2+str(days)+url3,header=4,parse_dates=True,
		skiprows=[5,6,7])
	# print df
 	pd.set_option('display.max_rows', 100)
 	if(days>1):
 		i=0
 		for i in range(2,len(df)):
 			# print df.iat[i,0]
 			if(str(df.iat[i,0]).startswith('a')): 
 				# print "the next day readings start form " + str(df.iat[i,0])
 				df.iat[i,0] = df.iat[i,0][1:]
 			try:
 				if(int(df.iat[i,0])-int(df.iat[i-2,0])<0): 
 					break
 			except:
 				print df
 				continue
 		#i=df.index.get_loc('a',method='ffill')
 		df=df.ix[0:i-2]
 	# print df
 	df.columns = ['DATE', 'CLOSE','HIGH','LOW','OPEN','VOLUME']
	df=df.set_index('DATE')
	#print df
	return df

def read_list(name = "Equity", list = []):
	if(len(list)>0):
		df = pd.read_csv("Data/"+name+".csv", usecols = list)
	else:
		df = pd.read_csv("Data/"+name+".csv")
	return df

def save_list(df):
	df.to_csv("Data/Latest_List.csv",mode='w',index=False)

def add_to_blacklist(quote,new=False):
	#df = pd.read_csv("Blacklist.csv",names=['SYMBOL'],header=None)
	#if os.stat("Blacklist.csv").st_size > 0:
	#Above line can be used to know if file empty or not
	if(new):
		quote.to_csv("Data/Blacklist.csv",mode='w',index=False)
	else:quote.to_csv("Data/Blacklist.csv",mode='a',header=False , index=False)
    
def blacklisted(symbol,blacklist):
	# blacklist = read_list("Blacklist")
	if any(blacklist['SYMBOL'] == symbol): 
		#print df
		return True
	else: return False


def tokenize(df):
	# lst = list(df.columns.values)
	# lst.append("instrument_token")
	# df.columns=lst
	# df = df.query('RESULT != 0')
	df.loc[:,'instrument_token'] = 0
	tdf = read_list("Instruments",['instrument_token','tradingsymbol'])
	for i,row in df.iterrows():
		r = tdf.loc[tdf['tradingsymbol'] == row['SYMBOL']].values
		#x=  r.iloc[0]['instrument_token']
		df.set_value(i,'instrument_token',int(r[0][0]))
		
	return df

def get_symbol(list):
	sym = []
	tdf = read_list("Instruments",['instrument_token','tradingsymbol'])
	for x in range(0,len(list)):
		r = tdf.loc[tdf['instrument_token'] == list[x]].values
		sym.append(r[0][1])
	return sym

def get_token(sym):
	tdf = read_list("Latest_List",['SYMBOL','instrument_token'])
	r = tdf.loc[tdf['SYMBOL'] == sym].values
	return r[0][1]


