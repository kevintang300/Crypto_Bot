"""

Exponential Moving Average


    1. What does an exponential moving average do?

        First, let us understand what a moving average is and how it could be useful for
        traders and during stock analysis.

            Moving Average
            ---------------
            
            A moving average cuts down the amount of "noise" on a price chart.
            The moving average can help detect a trend/direction the chart is moving. In other
            words, moving averages help detect uptrends/downtrends during a specified time 
            period.

            If the current price is above the average then there's an uptrend. Otherwise if
            the price is below the average then there is a downtrend.


            Why Exponential Moving Average?
            -------------------------------

            There are many types different types of moving averages and there are pros/cons
            for each ones. I decided on exponential moving averages because it places a 
            greater weight on the most recent prices. 


    2. How is the exponential moving average caluclated? 


        The EMA formula is calulated using the previous day's EMA. Since we need to start
        our calculations somewhere, we need to have a starter EMA, in other words an 
        "initial ema".


            Step 1 - Calculating Initial EMA
            --------------------------------

            The intial ema is just the simple moving average (sma). To calculate the sma,
            you must add all closing prices for each day in the given period and divide it
            by the number of days.

            Example:

            Period = 5 days
            simple moving average = (x1 + x2 + x3 + x4 + x5) / 5
            intial ema = simple moving average

            Edit: I realized there are various sources that are mentioning that an inital ema can be initalized/started
            in many different ways. To simplify things, my inital ema will be the very first closing price within my 
            range of days.



            Step 2 - Smoothing constant/Weighting multiplier
            -------------------------------------------------

            Smoothing constant is what emphasizes the most recent data, we'll need it for
            the formula

            smoothing factor = 2 / (number of time periods + 1)


            Step 3 - Final calculations
            ----------------------------

            EMA = (current closing price * smoothing_factor) + previous day's ema * (1-smoothing_factor)

"""



class EMA:

    def __init__(self, closing_prices, period):
        
        self.closing_prices = closing_prices
        self.period = period
        self.smoothing_factor = 2 / (int(self.period) + 1)
        
        self.ema_calculations = []
        
    
    #Simple Moving Average - CURRENT UNUSED
    def __calculate_sma(self):

        total_sum = 0
        n = len(self.closing_prices)

        for i in range(n):
            c_price = float(self.closing_prices[i])
            total_sum += c_price
        
        return total_sum / int(self.period)

    #Get's the initial list of ema's needed for future calculations
    def initalize_starting_ema(self):

        n = len(self.closing_prices)

        initial_ema = float(self.closing_prices[0])
        self.ema_calculations = [initial_ema]

        for i in range(1,n):
            c_price = float(self.closing_prices[i])
            ema_formula = (c_price * self.smoothing_factor) + self.ema_calculations[i-1] * (1-self.smoothing_factor)

            self.ema_calculations.append(ema_formula)
    

    def calculate_ema(self, closing_price):

        cur_ema = (float(closing_price) - self.ema_calculations[-1]) + self.smoothing_factor + self.ema_calculations[-1]
        self.ema_calculations.append(cur_ema)
        return cur_ema

    def detect_trend(self):
        return 0
        

    



