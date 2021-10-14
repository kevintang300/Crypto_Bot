class BinanceAPI:

    def __init__(self):

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

    """

    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'

    """

    #Use client object to gather information on historical and current numbers of the market.
    def get_chart(self, period, symbol, client):

        if client != None:
            self.__historical_data = client.get_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, str(period) + " day ago UTC")

            self.open_prices = [open_price[1] for open_price in self.__historical_data]
            self.high_prices = [high_price[2] for high_price in self.__historical_data]
            self.low_prices = [low_price[3] for low_price in self.__historical_data]
            self.closing_prices = [close_price[4] for close_price in self.__historical_data]
            self.volumes = [vol[5] for vol in self.__historical_data]

            self.support = min(self.low_prices)
            self.resistance = max(self.high_prices)

            self.most_recent_closing = self.closing_prices[-1]
            self.current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])

    def get_closing_prices(self):
        return self.closing_prices
        


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
