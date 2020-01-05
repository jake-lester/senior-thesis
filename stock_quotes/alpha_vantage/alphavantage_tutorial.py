from alpha_vantage.timeseries import TimeSeries
import alpha_vantage_parameters
import pandas as pd

# Your key here
key = alpha_vantage_parameters.API_KEY
ts = TimeSeries(key)
aapl, meta = ts.get_intraday(symbol="AAPL", interval="1min", outputsize="compact")
#aapl, meta = ts.get_daily(symbol='AAPL')
#print(aapl['2019-09-12'])
#print(meta)

df = pd.DataFrame.from_dict(aapl, orient='index')
print(df.head())