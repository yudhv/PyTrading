import matplotlib.pyplot as plt
import webbrowser

def plot_close(title = 'Stock Prices per Minute'):
	# df1 = df.ix[0:,'CLOSE']
	# ax = df1.plot(title=title, fontsize=10)
	# ax.set_xlabel('DATE')
	# ax.set_ylabel('CLOSE')
	# plt.show()
	url="https://www.google.com/finance?q=NSE%3A"
	chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
	webbrowser.get(chrome_path).open(url+title)

def plot_change_hist(df):
	ax=df['Percent Change'].hist(bins=100)
	mean = df['Percent Change'].mean()
	std = df['Percent Change'].std()
	ax.set_xlabel('CHANGE')
	ax.set_ylabel('FREQUENCY')
	plt.axvline(mean,color='g',linestyle='dashed',linewidth=2)
	plt.axvline(std,color='r',linestyle='dashed',linewidth=2)
	plt.axvline(-std,color='r',linestyle='dashed',linewidth=2)
	plt.show()