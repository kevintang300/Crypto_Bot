from binance import Client, BinanceSocketManager
import asyncio
import sys
import json
import time
from datetime import date
import matplotlib.pyplot as plt


"""
API RATE LIMIT
--------------
- 1200 Requests/minute
- 10 orders/second
- 100000/24hours
"""

class CryptoTrader:

    def _init_(self):

        self.__api_key
        self.__secret_key
        self.__accountBalance = None

        self.client = self.cr_client()
        self.currentPrice = -1
        self.date = None
        self.startDate = None

        self.__period = None
        self.__smoothingFactor = None
        self.__fibRatios = [0, 0.236, 0.382, 0.50, 0.618, 0.786, 1]
        self.__fibExtensions = [1.382, 1.50, 1.618, 1.78]


    def today_date(self):
        today = date.today()
        self.date = today.strftime("%d %B %Y")

    def start_date(self):
        dateList = self.date.split(" ")
        day = int(dateList[0]) - (self.__period-1)
        self.startDate =  str(day) + " " + dateList[1]  + " " + dateList[2]

    def get_initial_ema(self, klineData):
       return float(klineData[0][4])

    def calculate_ema(self, klineData, initialEMA):
        EMA = [initialEMA]
        i = 1
        n = len(klineData)
        while i < n:
            closingPrice = float(klineData[i][4])
            emaCalculation = (closingPrice * self.__smoothingFactor) + (EMA[i-1] * (1-self.__smoothingFactor))
            EMA.append(emaCalculation)           
            i = i + 1

        return EMA

    def graph(self, EMA, klineData, symbol):

        n = len(klineData)

        x = []
        y = []
        for i in range(len(klineData)):
            y.append(float(klineData[i][4]))
            x.append(i)
    

        plt.plot(x,y, label="Closing Prices")


        x2 = []
        y2 = []
        for i in range(len(EMA)):            
            x2.append(i)
            y2.append(EMA[i])
            
        plt.plot(x2,y2, label="EMA")    
        plt.title(symbol + " Trend Analysis")

        plt.legend()
        plt.show()

    def detect_trend(self, klineData, EMA):
        
        n = len(klineData)-1
        current_cp = float(klineData[n][4])
        current_ema = EMA[n]

        if current_cp > current_ema:
            return 1
        elif current_ema > current_cp:
            return -1
        else:
            return 0

    def get_resistance_support(self, klineData):

        closingPrices = []

        for eachList in klineData:
            closingPrices.append(float(eachList[4]))

        return max(closingPrices), min(closingPrices)

    def get_ratio(self, resistance, support, currentPrice, trend):

        ratioOne = resistance - support
        if trend == 1:
            uptrendRatio = currentPrice - support
            return (uptrendRatio/ratioOne)
        elif trend == -1:
            downtrendRatio = resistance - currentPrice
            return (downtrendRatio/ratioOne)
        
    def init_buy(self, resistance, support, currentPrice):
        
        buyAmount = .10 * self.__accountBalance
        self.__accountBalance  = self.__accountBalance - buyAmount



    def begin_trading(self):

        print("Trading Algorithm Beta_V1")
        print("Created by Kevin Tang")
        print("Date Created: June 10th, 2021\n\n")

        #Initializing Client
        #self.__api_key = input("API KEY: ")
        #self.__secret_key = input("Secret KEY: ")
        self.client = Client(tld='us') #pass in keys in param

        #Initializing Smoothing Factor for EMA calculation
        self.__period = 7 #Temp, CHANGE TO USER INPUT NEXT PUSH

        print("Currently supporting a 7 day period only.")
        print("Not requesting API key during beta version.")


        print("\n\nTrading ADAUSD")
        print("---------------")
        self.__smoothingFactor = 2/(self.__period+1)

        analysisCount = 0
        buyCount = 0
        sellCount = 0
        waitCount = 0

        #Only analyze market 360 times.
        while analysisCount < 360:
            print("Gathering Historical KLine Data...")
            klineData = self.client.get_historical_klines('ADAUSD', self.client.KLINE_INTERVAL_1MINUTE, str(self.__period) + " day ago UTC")
            initialEMA = self.get_initial_ema(klineData)
            EMA = self.calculate_ema(klineData, initialEMA) 

            trend = self.detect_trend(klineData, EMA) 


            resistanceLevel, supportLevel = self.get_resistance_support(klineData)
            currentPrice = float(self.client.get_symbol_ticker(symbol='ADAUSD')['price'])
            print("Current Price = ", currentPrice)
            print("Resistance Level = ", resistanceLevel)
            print("Support Level = ", supportLevel)

        
            print("Detecting Trend...")
            ratio = self.get_ratio(resistanceLevel, supportLevel, currentPrice, trend)
            print("Ratio =", ratio, end='')
            print(" during a ", end='')
            if trend == 0:
                print("Steady")
            elif trend == -1:
                print("Downtrend")
            else:
                print("Uptrend")

            
            if ratio > 0.50 and ratio < 0.62 and trend == 1:
                buyCount = buyCount + 1
    

            print("\n\nPreparing for next trade...")
            analysisCount = analysisCount + 1
            time.sleep(5)

        print("30 minute Trading Statistics")
        print("Buy Count: ", buyCount)
        print("Sell Count: ", sellCount)
        print("Wait Count: ", waitCount)

        #Plots the EMA graph
        #self.graph(EMA, klineData, 'ADAUSD')


        

c = CryptoTrader()
c.begin_trading()

        


