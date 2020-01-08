from alpha_vantage.timeseries import TimeSeries
import alpha_vantage_parameters
import pandas as pd
import time
import json
import matplotlib


class IntraDaySP500(TimeSeries):
    """
    gets the intraday quotes for sp500.
    returns a dictionary with each symbol as key
    has intraday for past week when on_stock_list() run on interval="1min", outputsize="full"
    returns a dictionary with each symbol as key, datafram as value.
    This dataframe is intraday and has format that can be seen on alphavantage
    #TODO make dataframe example in markdown
    """

    def on_stock(self, symbol, interval="60min", outputsize="compact"):
        # returns dataframe of single stock for current intraday quotes
        # TODO include other alphavantage params in on_stock params
        d, meta = self.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        #df = pd.DataFrame.from_dict(d, orient='index')
        print(d)
        return d

    def on_stock_list(self, symbols=alpha_vantage_parameters.SMALL_STOCK_LIST, interval="60min", outputsize="compact"):
        data = {}
        for s in symbols:
            data[s] = self.on_stock(s, interval, outputsize)
            time.sleep(15) #to circumvent alpharad limitter of 5 calls per minute, we make 4 calls per minute
        return data

def candlestick_plot(data, ticker):
    # make a candlestick plot


{"M": {"2020-01-08 13:28:00": {"1. open": "18.1650", "2. high": "18.1650", "3. low": "18.1250", "4. close": "18.1297", "5. volume": "124544"},
def save_to_file(data, data_filename):
    with open(data_filename, 'w') as fp:
        json.dump(data, fp)

if __name__ == "__main__":
    ts = IntraDaySP500(key=alpha_vantage_parameters.API_KEY)
    output = ts.on_stock_list(interval="1min",outputsize="full")
    save_to_file(output, "sp500_quotes\\small_sample.json")
    #print(output["APPL"])
