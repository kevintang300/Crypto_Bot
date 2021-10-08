from ema import EMA
from binance_api import BinanceAPI
from trader import Trader
import matplotlib.pyplot as plt
import time


class CryptocurrencyAnalyzer:
    
    def __init__(self, period, symbol, trading_time):

        self.period = period
        self.symbol = symbol
        self.trading_length = trading_time

    def __gather_input(self):
        
        self.period = input("How many days back would you like to analyze: ")

        self.symbol = input("What type of currency are you trying to trade: ")

        self.trading_length = input("How long would you like to trade for in minutes: ")
        self.trading_length = int(self.trading_length) * 60

    def trend_detection(self, cur_price, cur_ema):
        
        if cur_price >= cur_ema:
            print("Uptrend for", self.symbol)
        else:
            print("Downtrend for", self.symbol)

    def graph_ema(self, closing_prices, ema_array):

        #Plot the closing prices on the graph
        x = []
        y = []
        for i in range(len(closing_prices)):
            x.append(i)
            y.append( float(closing_prices[i]) )

        plt.plot(x,y, label="Closing Prices")


        #Now graph the moving averages on the graph
        x2 = []
        y2 = []
        for i in range(len(ema_array)):
            x2.append(i)
            y2.append(ema_array[i])


        plt.plot(x2,y2,label="EMA")
        plt.title(self.symbol + " Trend Analysis")
        plt.legend()
        plt.show()
        plt.close()



    def run(self, trader=None):

        #self.__gather_input()
        market = BinanceAPI('ADAUSD', self.period)
        market.connect_to_client()

        #Gather historical kline data's to initalize EMA list.
        market.update_data()
        ema_obj = EMA(market.closing_prices, 100)
        ema_obj.initalize_starting_ema()

        #self.graph_ema(market.closing_prices, ema_obj.ema_calculations) 

        

        """

        #Grab the current time
        start_time = time.time()

        while True:

            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > self.trading_length:
                break
            
            #Every iteration we'll be grabing in new data for to help with bot decision making.
            current_ema = ema_obj.calculate_ema(market.most_recent_closing)
            self.trend_detection(market.current_price, current_ema)
            #self.graph_ema(market.closing_prices, ema_obj.ema_calculations)
        """
        

trader = CryptocurrencyAnalyzer(100, "ADAUSD", 60)
trader.run()
    