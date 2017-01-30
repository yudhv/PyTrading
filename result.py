import pandas as pd
import os
from getter import read_list
from datetime import datetime
from termcolor import cprint
import math

def get(x=1):
	if(x==1):
		day=datetime.strftime(datetime.now(),'%d_%m_%Y')
		return read_list("Results/"+"18_10_2016")
	elif(x==2):
		return read_list("Test/5_test")
	

def profit_to_loss():
	os.system("clear")
	df = get(1)
	print df
	pr = 0.0
	prc = 0
	lsc = 0
	ls = 0.0
	res = 0
	for i in range(0,len(df)):
		res = math.floor(2000/df.at[i,'Buy_Price'])
		if(df.at[i,'Status'] == 'PROFIT'): 
			prc+=1
			pr += df.at[i,'Amount']#*res
		elif(df.at[i,'Status'] == 'LOSS'): 
			ls += df.at[i,'Amount']#*res
			lsc+=1
	cprint("Total Profit deals = %d"%(prc),"green")
	cprint("Total Loss Deals = %d\n "%(lsc),"red")
	cprint("Total Profit = %f"%(pr),"green")
	cprint("Total Loss = %f\n"%(ls),"red")
	cprint("Profit to Loss Ratio = %f\n"%(pr/ls),"blue",attrs=["bold","underline"])

def result():
	pd.set_option('display.max_rows', 1000)
 	
	profit_to_loss()
	# best_rand_comb()

def best_rand_comb():
	os.system("clear")
	df = get(2)
	# df = df.query('indi1 ==1 & indi2 ==1')
	# df = df['indi1']>1
	# print df
	res = pd.DataFrame(columns=['indi1','indi2','p_deals','l_deals','P','L','P/L'])
	print res
	for i in range(0,len(df)):
		i1 = str(df.loc[i,'indi1'])
		i2 = str(df.loc[i,'indi2'])
		re = math.floor(2000/df.at[i,'Buy_Price'])
		if(len(res.query("indi1 == "+i1 +"& indi2 == "+i2)) == 0):
			res.loc[len(res),'indi1']=int(i1)
			res.loc[len(res)-1,'indi2']=int(i2)
			if(df.loc[i,'Status'] == 'PROFIT'):
				res.loc[len(res)-1,'p_deals']=1
				res.loc[len(res)-1,'P'] = df.loc[i,'Amount']*re
				res.loc[len(res)-1,'L'] = 0.0
				res.loc[len(res)-1,'l_deals']=0
			else: 
				res.loc[len(res)-1,'l_deals']=1
				res.loc[len(res)-1,'L'] = df.loc[i,'Amount']*re
				res.loc[len(res)-1,'P'] = 0.0
				res.loc[len(res)-1,'p_deals']=0
		else:
			x = res.query("indi1 == "+i1 +"& indi2 == "+i2).index
			if(df.loc[i,'Status'] == 'PROFIT'):
				res.loc[x,'p_deals']+=1
				res.loc[x,'P'] += df.at[i,'Amount']*re
			else: 
				res.loc[x,'l_deals']+=1
				res.loc[x,'L'] += df.at[i,'Amount']*re
	res['P/L'] = res['P']/res['L']
	res = res.sort_values(by='P/L',ascending=False)
	res = res.reset_index(drop=True)
	print res
	
						
	# for i in range(1,11):
	# 	for j in range(1,11):
	# 		res.loc[len(res),'indi1'] = i
	# 		res.loc[len(res)-1,'indi2'] = j
	# 		temp = df.query('indi1 == '+ str(i)+' & indi2 =='+str(j) + '& Status == PROFIT')
	# 		res.loc[len(res)-1,'p_deals'] = len(temp)
	# 		temp = df.query('indi1 == '+ str(i)+' & indi2 =='+str(j) + '& Status == LOSS')
	# 		res.loc[len(res)-1,'l_deals'] = len(temp)
			





















