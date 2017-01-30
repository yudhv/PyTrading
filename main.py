from getter import read_list,blacklisted,download_data,tokenize,save_list,add_to_blacklist
from plotter import plot_change_hist,plot_close
from tester import make_list,append_list,change_adder,rejectable,sort_list
from kite_connect import kite_init,start_ticking
from result import result
from tick_data import show_data
from termcolor import cprint
import pandas as pd
import time
import os
if __name__ == "__main__":
	a=0
	all_stocks = read_list("Equity",['SYMBOL','NAME OF COMPANY'])
	lst = make_list()
	os.system("clear")

	while (a == 0):
		cprint("**********************************************************"
			,"grey",attrs=['bold'])
		cprint("\n0=>Make List\t\t\t1=>Show Last List\n","cyan",attrs=['bold'])
		cprint("2=>Show Graph\t\t\t3=>Show stock data","magenta",attrs=['bold'])
		cprint("4=>Show Histogram\t\t5=>Refine through History\n","magenta",
			attrs=['bold'])
		cprint("7=>Initialise Kite\t\t8=>Start Ticking\n","blue",attrs=['bold'])
		cprint("9=>Get Result\n","green",attrs=['bold'])
		cprint("11=>Update BlackList\n","grey",attrs=['bold'])
		cprint("**********************************************************"
			,"grey",attrs=['bold'])
		x = int(input(""))


		if(x==0):
			# lst = make_list()
			# blist = read_list("BlackList")
			# r1 = int(input("\nEnter start for range : "))
			# r2 = int(input("Enter end for range : "))
			# for i in range(r1,r2):
			# 	if(blacklisted(all_stocks.iat[i,0],blist) == False): 
			# 		df = download_data(all_stocks.iat[i,0],1)
			# 	else: continue
			# 	print all_stocks[i:i+1], "  %d"%len(df)
			# 	if(rejectable(df)): continue
			# 	#plot_close(df,all_stocks.iat[i,0])
			# 	df=change_adder(df)
			# 	lst=append_list(df,all_stocks.iat[i,0],lst)
			# 	#plot_change_hist(df)
			# 	time.sleep(0.5)
			# os.system("clear")
			# print "\n\nTHE LIST IS :"
			# lst = sort_list(lst)
			# lst = tokenize(lst)
			# save_list(lst)
			# print lst

			dframe = pd.DataFrame(columns=['SYMBOL', 'CLOSE','STD','VOLUME','RESULT'])
			blist = read_list("BlackList")
			r1 = int(input("\nEnter start for range : "))
			r2 = int(input("Enter end for range : "))
			for i in range(r1,r2):
				symbol = all_stocks.iat[i,0]
				if(blacklisted(symbol,blist) == True): continue
				df = download_data(symbol,1)
				if(rejectable(df)): continue
				# print symbol, "  %d"%len(df)
				# print df
				close = df['CLOSE'].mean()
				vol = df['VOLUME'].median()
				std_dev = df['CLOSE'].std()
				# temp_row = [symbol,close,std_dev, vol, pow(vol,2)/(close*std_dev)]
				temp_row = [symbol,close,std_dev, vol, vol/close]
				dframe.loc[len(dframe)] = temp_row
				print i+1
				time.sleep(0.5)
			dframe = dframe.sort_values(by='RESULT',ascending=False)
			dframe = dframe.reset_index(drop=True)
			dframe = tokenize(dframe)
			save_list(dframe)
			os.system("clear")
			print dframe

			continue

		if(x==1):
			lst = read_list("Latest_List")
			pd.set_option('display.max_rows', 300)
			print lst
			continue

		if(x==2):
			stoc = raw_input("Enter Stock Number or Quote\n")
			if stoc.isdigit():
				sym = lst.iat[int(stoc),0]
			else:
				sym = stoc.upper()
			plot_close(sym)
			os.system("clear")
			print lst
			continue

		if(x==3):
			lst = read_list("Latest_List")
			stoc = raw_input("Enter Stock Number or Quote\n")
			if stoc.isdigit():
				sym = lst.iat[int(stoc),0]
			else:
				sym = stoc.upper()
			# day = int(raw_input("Enter the day : "))
			# print lst.query("SYMBOL == "+sym)
			df = show_data(lst.query('SYMBOL == "%s"'%(sym)).iat[0,4])
			# df = download_data(sym,day)
			# df = change_adder(df)
			print df
			# print "Average Volume for %s is %f" %(sym,df['VOLUME'].median())
			# print "Mean for %s is %f" % (sym,df['Percent Change'].mean())
			# print "Kurtosis value for %s = %f\n" %(sym,df['Percent Change'].kurtosis())
			print lst
			continue

		if(x==4):
			stoc = raw_input("Enter Stock Number or Quote\n")
			if stoc.isdigit():
				sym = lst.iat[int(stoc),0]
			else:
				sym = stoc.upper()
			day = int(raw_input("Enter the day : "))
			df = download_data(sym,day)
			df = change_adder(df)
			plot_change_hist(df)
			os.system("clear")
			print lst
			continue

		if(x==5):
			days = int(input("Enter the number of days you want to go back : "))
			for x in range(0,len(lst)):
				res,mean,kurt = calculate_result(lst.iat[x,0],days)
				lst.iat[x,3] = res
				lst.iat[x,1] = mean
				lst.iat[x,2] = kurt
			lst = sort_list(lst)
			#lst.columns = ['SYMBOL','MEAN CHANGE(upd)','STD','KURTOSIS(upd)','RESULT(upd)']
			print lst
			save_list(lst)
			continue

		# if(x==6):
		# 	stoc = raw_input("Enter Stock Number or Quote\n")
		# 	if stoc.isdigit():
		# 		sym = lst.iat[int(stoc),0]
		# 	else:
		# 		sym = stoc.upper()
		# 	day = int(raw_input("Enter the day : "))
		# 	df = download_data(sym,day)
		# 	df = change_adder(df)
		# 	make_oscillator(df)
		# 	continue

		if(x==7):
			kite_init()
			continue

		if(x==8):
			start_ticking()
			continue

		if(x==9):
			result()
			continue


		if(x==11):
			r1 = int(input("\nEnter start for range : "))
			r2 = int(input("Enter end for range : "))
			if(r1 == 0): new = True
			else: new = False
			for i in range(r1,r2):
				df = download_data(all_stocks.iat[i,0],1)
				# print df
				if(len(df)<=75):
					add_to_blacklist(all_stocks[i:i+1],new)
					new = False
					print all_stocks[i:i+1]+"  "+str(len(df))
				time.sleep(0.2)
					

		else:
			os.system("clear")
			a=1

	 