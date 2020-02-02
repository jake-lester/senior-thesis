from wallstreet import Stock, Call, Put

#overide source since google_finance no longer is compatible

class Stream():
    """
    This streams real time stock quotes
    """

    def __init__(self, ticker, src='yahoo'):
        