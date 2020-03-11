import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['figure.titlesize'] = 18
plt.rcParams['figure.titleweight'] = 'medium'
plt.rcParams['lines.linewidth'] = 2.5

#### make a funcion that lets you specify a few parameters and calculates the payoff
# S = stock underlying # K = strike price # Price = premium paid for option
# Long Call Payoff = max(Stock Price - Strike Price, 0)     # If we are long a call, we would only elect to call if the current stock price is greater than     # the strike price on our option
def long_call(S, K, Price):
    P = list(map(lambda x: max(x - K, 0) - Price, S))
    return P


def long_put(S, K, Price):
    # Long Put Payoff = max(Strike Price - Stock Price, 0)     # If we are long a call, we would only elect to call if the current stock price is less than     # the strike price on our option
    P = list(map(lambda x: max(K - x, 0) - Price, S))
    return P


def short_call(S, K, Price):
    # Payoff a shortcall is just the inverse of the payoff of a long call
    P = long_call(S, K, Price)
    return [-1.0 * p for p in P]


def short_put(S, K, Price):
    # Payoff a short put is just the inverse of the payoff of a long put
    P = long_put(S, K, Price)
    return [-1.0 * p for p in P]


def binary_call(S, K, Price):
    # Payoff of a binary call is either:     # 1. Strike if current price > strike     # 2. 0
    P = list(map(lambda x: K - Price if x > K else 0 - Price, S))
    return P


def binary_put(S, K, Price):
    # Payoff of a binary call is either:     # 1. Strike if current price < strike     # 2. 0
    P = list(map(lambda x: K - Price if x < K else 0 - Price, S))
    return P


S = [t/5 for t in range(0,1000)] # Define some series of stock-prices
fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, figsize = (20,15))
fig.suptitle('Payoff Functions for Long/Short Put/Calls', fontsize=20, fontweight='bold')
fig.text(0.5, 0.04, 'Stock/Underlying Price ($)', ha='center', fontsize=14, fontweight='bold')
fig.text(0.08, 0.5, 'Option Payoff ($)', va='center', rotation='vertical', fontsize=14, fontweight='bold')


lc_P = long_call(S,100, 10)
plt.subplot(221)
plt.plot(S, lc_P, 'b')
plt.legend(["Long Call"])




lp_P = long_put(S,100, 10)
plt.subplot(222)
plt.plot(S, lp_P, 'r')
plt.legend(["Long Put"])

sc_P = short_call(S,100, 10)
plt.subplot(223)
plt.plot(S, sc_P, 'b')
plt.legend(["Short Call"])

sp_P = short_put(S,100, 10)
plt.subplot(224)
plt.plot(S, sp_P, 'r')
plt.legend(["Short Put"])

plt.show()