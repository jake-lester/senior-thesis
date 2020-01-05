# Variables for alpha_vantage authorization and variable passing
import pandas as pd
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

SP500_SYMBOLS = table[0].loc[1:,0].tolist()
API_KEY = "DKAEZH76GPPYMHHF"

print(len(SP500_SYMBOLS))