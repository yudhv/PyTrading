from datetime import datetime
from getter import get_symbol
import json
import pandas as pd
import math
import sys

# check to see if the below declaration is even necessary

latest_trigger_list = []
pnl_list = []

def make_list(sub_list):
	global latest_trigger_list
	global pnl_list 
	latest_trigger_list = pd.DataFrame(data={'last_price':0.0,'mode':'None',
		'quote':0.0,'time':'00:00:00'},
		index=sub_list)
	pnl_list = pd.DataFrame(columns=['Status','Mode','Buy_Price','Sell_Price',
		'Stock','Amount','Buy_Time','Sell_Time'])
	name = "Data/Results/"+get_time('d')+".csv"
	file = open(name,"a+")
	file.close()
	# try using append mode so that testing doesn't interrupt the acquisition of data
	pnl_list.to_csv(name,mode='a',index=False)
# 	latest_list = pd.DataFrame({'last_price': 970.1, 'volume': 140492, 
# 	'sell_quantity': 142345, 'last_quantity': 7, 
# 	 'high': 970.5,  'low': 965.0,
# 	  'bp1':0.0,'bo1':0.0,'bq1':0.0,'ap1':0.0,'ao1':0.0,'aq1':0.0,
# 	   'bp2':0.0,'bo2':0.0,'bq2':0.0,'ap2':0.0,'ao2':0.0,'aq2':0.0,  
# 	 'buy_quantity': 118215, 'instrument_token': 738561},index=[0])

# # The below is done to set the order of the columns

# 	latest_list.columns = ['last_price', 'volume', 
# 	'sell_quantity', 'last_quantity',  
# 	 'high', 
# 	'low', 'bp1','bo1','bq1','ap1','ao1','aq1',
# 	'bp2','bo2','bq2','ap2','ao2','aq2',  
# 	 'buy_quantity', 'instrument_token']
	# latest_list.index = sub_list
	# latest_list['instrument_token'] = sub_list
	print latest_trigger_list

def check_trigger(fr):
	global latest_trigger_list
	if(fr[11]==0 or fr[17]==0 or fr[8]==0 or fr[14]==0):
		return
	result = fr[8]/(fr[11]+fr[17])
	benchmark = 100
	result = result*100/benchmark
	time = get_time('h')
	stock = get_symbol([fr[19]])

	indi1 = 9
	indi2 = 1

	if(fr[8]/fr[11]>=indi1 and fr[8]/fr[17]>=indi2):
		print "%s =>  BUY %s at %f"%(time,stock,fr[9])
		# Here lies the code for updating the list
		latest_trigger_list.at[fr[19],'mode'] = 'BUY'
		latest_trigger_list.at[fr[19],'quote'] = fr[9]
		latest_trigger_list.at[fr[19],'time'] = fr[20]
		
		# data = []
		# data.append({'time': time, 'stock' : stock, 'mode': 'BUY', 'price': fr[9]})
		# # data['time'] = time
		# # data['stock'] = stock
		# # data['mode'] = 'BUY'
		# # data['price'] = fr[9]
		# json_data = json.dumps(data)
		# with open('Data/Triggers.txt', 'a') as outfile:
		# 	json.dump(json_data, outfile)

	if(fr[11]/fr[8]>=indi1 and fr[11]/fr[14]>=indi2):
		print "%s =>  SELL %s at %f"%(time,stock,fr[6])
		# Here lies the code for updating the list
		latest_trigger_list.at[fr[19],'mode'] = 'SELL'
		latest_trigger_list.at[fr[19],'quote'] = fr[6]
		latest_trigger_list.at[fr[19],'time'] = fr[20]
		
		# data = []
		# data.append({'time': time, 'stock' : stock, 'mode': 'SELL', 'price': fr[6]})
		# # data['time'] = time
		# # data['stock'] = stock
		# # data['mode'] = 'SELL'
		# # data['price'] = fr[6]
		# json_data = json.dumps(data)
		# with open('Data/Triggers.txt', 'a') as outfile:
		# 	json.dump(json_data, outfile)

def check_latest_trigger_list(fr):

	global latest_trigger_list
	global pnl_list
	# experiment with more logic to this, like also checking for last bid and ask 
	# prices to improve accuracy

	# print fr
	mode = latest_trigger_list.at[fr[19],'mode']
	if(mode != 'None'):
		#Calculate the result of prediction
		if(latest_trigger_list.at[fr[19],'last_price'] != fr[0]):
			res = (fr[0] - latest_trigger_list.at[fr[19],'quote'])
			stat = ''
			
			if((res > 0.00) & (mode == 'BUY')):
				# res *= math.floor(2000/latest_trigger_list.at[fr[19],'quote'])
				stat = 'PROFIT'
				
			elif((res >= 0.1) & (mode == 'SELL')):
				stat = 'LOSS'
				

			elif((res < 0.00) & (mode == 'SELL')):
				res = -res
				stat = 'PROFIT'
				
			
			elif((res <= -0.1) & (mode == 'BUY')):
				res = -res
				stat = 'LOSS'

			else: return False

			pnl_list.loc[len(pnl_list),'Stock'] = get_symbol([fr[19]])
			pnl_list.loc[len(pnl_list)-1,'Sell_Time'] = get_time('h')
			pnl_list.loc[len(pnl_list)-1,'Buy_Time'] = latest_trigger_list.at[fr[19],'time']
			pnl_list.loc[len(pnl_list)-1,'Mode'] = mode
			pnl_list.loc[len(pnl_list)-1,'Buy_Price'] = latest_trigger_list.at[fr[19],'quote']
			pnl_list.loc[len(pnl_list)-1,'Sell_Price'] = fr[0]
			pnl_list.loc[len(pnl_list)-1,'Status'] = stat
			pnl_list.loc[len(pnl_list)-1,'Amount'] = res
			print pnl_list[len(pnl_list)-1:len(pnl_list)]

			name = "Data/Results/"+get_time('d')+".csv"
			pnl_list[len(pnl_list)-1:len(pnl_list)].to_csv(name,mode='a',
				header=False,index = False)
			latest_trigger_list.at[fr[19],'last_price'] = fr[0]
			latest_trigger_list.at[fr[19],'mode'] = 'None'
			latest_trigger_list.at[fr[19],'quote'] = 0.0
			return True

		else:
			return False

	else:
		latest_trigger_list.at[fr[19],'last_price'] = fr[0]
		return True


def get_time(form = 'd'):
	if(form == 'd'):
		return datetime.strftime(datetime.now(),'%d_%m_%Y')
	elif(form == 'h'):
		return datetime.strftime(datetime.now(), '%H:%M:%S')

def write_full_pnl():
	global pnl_list
	name = "Data/Results/"+get_time('d')+".csv"
	file = open(name,"a+")
	file.close()
	# try using append mode so that testing doesn't interrupt the acquisition of data
	pnl_list.to_csv(name,mode='w',index=False)


