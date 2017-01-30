from tick_data import *
from datetime import datetime
from getter import get_symbol
import json
import pandas


def check_trigger(fr):
	if(fr[11]==0 or fr[17]==0 or fr[8]==0 or fr[14]==0):
		return
	result = fr[8]/(fr[11]+fr[17])
	benchmark = 100
	result = result*100/benchmark
	time = datetime.strftime(datetime.now(), '%H:%M:%S')
	stock = get_symbol([fr[19]])
	if(fr[8]/fr[11]>=5 and result>=3):
		print "%s =>  BUY %s at %f"%(time,stock,fr[9])
		data = []
		data.append({'time': time, 'stock' : stock, 'mode': 'BUY', 'price': fr[9]})
		# data['time'] = time
		# data['stock'] = stock
		# data['mode'] = 'BUY'
		# data['price'] = fr[9]
		json_data = json.dumps(data)
		with open('Data/final.txt', 'a') as outfile:
			json.dump(json_data, outfile)

	if(fr[11]/fr[8]>=5 and fr[11]/(fr[8]+fr[14])>=3):
		print "%s =>  SELL %s at %f"%(time,stock,fr[6])
		data = []
		data.append({'time': time, 'stock' : stock, 'mode': 'SELL', 'price': fr[6]})
		# data['time'] = time
		# data['stock'] = stock
		# data['mode'] = 'SELL'
		# data['price'] = fr[6]
		json_data = json.dumps(data)
		with open('Data/final.txt', 'a') as outfile:
			json.dump(json_data, outfile)

def 
