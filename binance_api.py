from binance import Client, BinanceSocketManager

class BinanceAPI:

    def __init__(self, symbol, period):

        self.period = period
        self.symbol = symbol
        self.client = None

        """
        Historical Data is a list of lists
        ----------------------------------
        Index 1: Opening Price
        Index 2: High Price
        Index 3: Low price
        Index 4: Closing Price
        Index 5: Volume

        """
        self.__historical_data = None
        self.open_prices = None
        self.high_prices = None
        self.low_prices = None
        self.closing_prices = None
        self.volumes = None

        self.support = None
        self.resistance = None
        
        self.most_recent_closing = None
        self.current_price = None
    
       
    #Obtaining a client object to further use for grabbing information/data from Binance's exchange.
    def connect_to_client(self, api_key=None, api_secret=None):

        #Client connection without user account access
        if api_key == None or api_secret == None:
            self.client = Client(tld='us') #Using Binance.us in the United States
            print("Connection to Client Successful\n")
        else:
            self.client = Client(api_key, api_secret, tld='us')
            print("Connection to Client/Account Successful\n")

    #Use client object to gather information on historical and current numbers of the market.
    def update_data(self):

        if self.client != None:
            self.__historical_data = self.client.get_historical_klines(self.symbol, self.client.KLINE_INTERVAL_1DAY, str(self.period) + " day ago UTC")

            self.open_prices = [open_price[1] for open_price in self.__historical_data]
            self.high_prices = [high_price[2] for high_price in self.__historical_data]
            self.low_prices = [low_price[3] for low_price in self.__historical_data]
            self.closing_prices = [close_price[4] for close_price in self.__historical_data]
            self.volumes = [vol[5] for vol in self.__historical_data]

            self.support = min(self.low_prices)
            self.resistance = max(self.high_prices)

            self.most_recent_closing = self.closing_prices[-1]
            self.current_price = float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])

    """
    Print

    1. Opening Price
    2. High Price
    3. Low Price
    4. Close Price
    5. Volume

    OHLCV

    """
    def printOHLCV(self):
        
        print("Opening:", self.open_prices, "\n")
        print("High:", self.high_prices, "\n")
        print("Low:", self.low_prices, "\n")
        print("Closing:", self.closing_prices, "\n")
        print("Volumes:", self.volumes, "\n")
