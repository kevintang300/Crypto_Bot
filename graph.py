import matplotlib.pyplot as plt

class Graph:

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
        plt.legend()
        plt.show()
        plt.close()

    def interval_calculations(self, interval):

        num = None
        in_type = None
        HOURS_PER_DAY = 24
        MINUTES_PER_HOUR = 60

        if(len(interval) == 2):
            num = int(interval[0])
            in_type = interval[1]

        elif(len(interval) == 3):
            num = int(interval[0] + interval[1])
            in_type = interval[2]


        if in_type == 'm':
            total_prices_in_hour = MINUTES_PER_HOUR / num
            total_prices_in_day = total_prices_in_hour * HOURS_PER_DAY
            return total_prices_in_day

        elif in_type == 'h':
            total_prices_in_day = HOURS_PER_DAY  / num
            return total_prices_in_day

        else:
            return 0
             
        
    def graph_ema_crossover(self, larger_period, interval, cprices=None, cprices_two=None, ema_one=None, ema_two=None):
        
        x_axis_limit = self.interval_calculations(interval) * larger_period

        print(x_axis_limit)
        plt.xlim(0, x_axis_limit)
        plt.show()

