#PyTrading-a home-built High Frequency Trading system
##Overview
PyTrading is a project made out of a curiosity to understand the stock market. It is meant to identify highly liquid and low priced stocks from those listed in the Indian stock exchange NSE. Using the brokerage services of Kite Connect and Zerodha, tick data is generated and saved in-order to identify patterns for future bullish (or bearish) trends. 
The code does the following (in the same order):

0. Identify stocks that are best suited for High Frequency Trading (i.e high volume and low quoting price)
  * Google Finance and its interday data for NSE stocks is used to get this information
1. View last saved list of identified stocks
2. View a particular stock on Google Finance (only Chrome supported for now).
3. View Google Finance Raw data
4. Get a histogram view of a particular stock's data
5. Re-arrange the identified stock list by leveraging older data
6. Initialise the kite instance (NOTE-this requires an API key/secret key combination to run successfully)
7. Start the process of downloading and processing tick data for the identified stocks (this is where HFT logic is employed)
8. Process a simulated result from past saved tick data

##Dependencies
* pandas
* matplotlib
* numpy
* cprint
* kiteconnect
