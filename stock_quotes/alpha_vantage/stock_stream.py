from alpha_vantage.timeseries import TimeSeries
import alpha_vantage_parameters
import pandas as pd
import time


class IntraDaySP500(TimeSeries):
    """
    gets the intraday quotes for sp500.
    returns a dictionary with each symbol as key, datafram as value.
    This dataframe is intraday and has format that can be seen on alphavantage
    #TODO make dataframe example in markdown
    """

    def on_stock(self, symbol, interval="60min", outputsize="compact"):
        # returns dataframe of single stock for current intraday quotes
        # TODO include other alphavantage params in on_stock params
        d, meta = self.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        df = pd.DataFrame.from_dict(d, orient='index')
        return df

    def on_stock_list(self, symbols=alpha_vantage_parameters.SP500_SYMBOLS, interval="60min", outputsize="compact"):
        data = {}
        for s in symbols:
            data[s] = self.on_stock(s, interval, outputsize)
            time.sleep(15) #to circumvent alpharad limitter of 5 calls per minute, we make 4 calls per minute
        return data


if __name__ == "__main__":
    ts = IntraDaySP500(key=alpha_vantage_parameters.API_KEY)
    output = ts.on_stock_list()
    print(output["APPL"])
