from kiteconnect import WebSocket
from getter import read_list,get_symbol,get_token
from real_time import check_trigger,make_list,check_latest_trigger_list,get_time
import csv
from datetime import datetime
import json
import pickle
import pandas as pd
import logging
logging.basicConfig()

tick_df = []
subscribtion_list = []

# Callback for tick reception.
def on_tick(tick, ws):
	# print "IN TICK"
	# print "Length of tick is %d\n"%len(tick)
	global tick_df
	for z in range(0,len(tick)): 
		frames = []
		# print z
		for x, y in tick[z].iteritems():#try use nonlabel indexes to reduce overhead
			# print "x is ",x,"and y is ",y
			if x=='ohlc' or x=='depth' :
				if(x == 'ohlc'):
					for val,v in y.iteritems():
						if(val == 'high' or val == 'low'):
							frames.append(v)
						# print "value is ",v

				elif(x == 'depth'):
					# print "IN DEPTH NOW"
					for a in range(0,2):
						frames.append(tick[z][x]['sell'][a]['price'])
						frames.append(tick[z][x]['sell'][a]['orders'])
						frames.append(tick[z][x]['sell'][a]['quantity'])
						
						frames.append(tick[z][x]['sell'][a+5]['price'])
						frames.append(tick[z][x]['sell'][a+5]['orders'])
						frames.append(tick[z][x]['sell'][a+5]['quantity'])
			else:
				# print x
				if(x=='change' or x=='average_price' or x=='mode' or x=='tradeable'):
					continue
				frames.append(y)
		# print "BEFORE CHECK"
		frames.append(get_time('h'))
		if(check_latest_trigger_list(frames)): 
			check_trigger(frames)
		tick_df.loc[len(tick_df)] = frames
		# print "OUT TICK"
		
	# print tick_df
	if (len(tick_df)>110):  	#Total bytes = 164, Bytes used = 68, 8000/68 ~118
		save_ticks(tick_df)
		# print tick_df
		tick_df = tick_df.query('last_price == -1.0')


def save_ticks(df):
	name = "Data/Tick/"+datetime.strftime(datetime.now(),'%d_%m_%Y')+".csv"
	df.to_csv(name,mode='a',header=False , index=False)
	# make_tick_df()

def make_tick_file(x='y'):
	global tick_df
	name = "Data/Tick/"+datetime.strftime(datetime.now(),'%d_%m_%Y')+".csv"
	if x=='y':
		tick_df.to_csv(name,mode='w',index=False)

# Callback for successful connection.
def on_connect(ws):
    global subscription_list
    ws.subscribe(subscription_list)
    print "Subscribed to ",get_symbol(subscription_list)

    ws.set_mode(ws.MODE_FULL, subscription_list)

def make_tick_df():
	global tick_df 
# The below is done to set the order of the columns

	tick_df= pd.DataFrame(columns=['last_price', 'volume', 
	'sell_quantity', 'last_quantity',  
	 'high', 
	'low', 'bp1','bo1','bq1','ap1','ao1','aq1',
	'bp2','bo2','bq2','ap2','ao2','aq2',  
	 'buy_quantity', 'instrument_token','timestamp'])

def set_subscription_list(x):
	df = read_list("Latest_List",['instrument_token'])
	global subscription_list 
	subscription_list = df['instrument_token'].tolist()
	subscription_list = subscription_list[0:x]
	make_list(subscription_list)

def show_data(x):
	df = read_list("Tick/"+get_time(),
		['last_price','volume','bp1','bo1','bq1','ap1','ao1','aq1',
		'bp2','bo2','bq2','ap2','ao2','aq2','instrument_token','timestamp'])		
	df = df.query('instrument_token == '+str(x))
	pd.set_option('display.max_rows', len(df))
	print df


def save_instruments(kit):
	csv_dump = kit.instruments()
	csv_columns = ['instrument_token', 'exchange_token', 'tradingsymbol','name',
	 'last_price', 'expiry', 'strike', 'tick_size', 'lot_size', 'instrument_type',
	  'segment', 'exchange']
	with open("Data/Instruments.csv",'w') as ins:
		writer = csv.DictWriter(ins,fieldnames = csv_columns)
		writer.writeheader()
		for row in csv_dump:
			if(row['instrument_type'] == 'EQ' and row['exchange'] == 'NSE'):
				writer.writerow(row)

# Initialise.
def tick_init(api_key, public_token, id):
	kws = WebSocket(api_key, public_token, id)
	make_tick_df()
	#Remove below line before restarting in order to save data
	make_tick_file()
	num = int(input("Enter the number of stocks to subscribe\n"))
	set_subscription_list(num)
	# Assign the callbacks.
	kws.on_tick = on_tick
	kws.on_connect = on_connect

	# Infinite loop on the main thread. Nothing after this will run.
	# You have to use the pre-defined callbacks to manage subscriptions.
	kws.connect(True)




