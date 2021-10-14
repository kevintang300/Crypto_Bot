from ema import EMA
from binance_api import BinanceAPI
from trader import Trader
from graph import Graph
import time


from binance import Client, BinanceSocketManager

class CryptocurrencyAnalyzer:
    
    def __init__(self):

        self.period_one = None
        self.period_two = None
        self.interval = None

        self.symbol = None
        self.trading_length = None

    def __gather_input(self):
        
        self.period = input("How many days back would you like to analyze: ")
        self.symbol = input("What type of currency are you trying to trade: ")



    def __choose_analysis_type(self):

        option_chosen = input("1. Detecting Trend with Exponential Moving Average\n2. Fibonacci Retracement\n")
        return option_chosen


    def __trend_detection(self, cur_price, cur_ema):
        
        if cur_price >= cur_ema:
            
            cur_ema =  "{:.2f}".format(cur_ema)
            cur_price = "{:2f}".format(cur_price)
            print("\n\nCurrent Price of", self.symbol, "is " + str(cur_price))
            print("The most recent exponential moving average is at " + str(cur_ema))
            print("There is currently an uptrend for " + self.symbol, "over a " + str(self.period) + " day period")
            
        else:
            print("Downtrend for", self.symbol)

    def __ema_analysis(self, market, client):
        
        #KLINE chart for given symbol and period time range.
        market.get_chart( int(self.period), self.symbol, client)

        #EMA object will help initalize ema elements.
        ema = EMA(market.closing_prices, int(self.period))
        ema.initalize_starting_ema()

         #Current price is required for trend analysis.
        current_price =  float(client.get_symbol_ticker(symbol=self.symbol)['price'])
        self.__trend_detection(current_price, ema.ema_calculations[-1])

        #Visual Graph 
        g = Graph()
        g.graph_ema(market.closing_prices, ema.ema_calculations)
        



    def run(self, trader=None):

        #self.graph_ema(market.closing_prices, ema_obj.ema_calculations) 
        client = Client(tld="us")
        market = BinanceAPI()

        while True:
            analysis_pick = self.__choose_analysis_type()

            if analysis_pick == "1":
                self.__gather_input() #Get period and symbol
                self.__ema_analysis(market, client)
            elif analysis_pick == "2":
                print("Fibonacci Retracement Chosen")

        


        

trader = CryptocurrencyAnalyzer()
trader.run()
    