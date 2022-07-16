import pandas as pd
import yfinance as yf
from datetime import date
import os
today = date.today()

def pullTickerData(ticker, start, end):
    tickerData = yf.download(ticker, start, end)
    tickerData.to_csv(ticker + '_data.csv')

def formatDate(year, month, date):
    if month<10:
        month = "0"+str(month)
    if date<10:
        date = "0"+str(date)
    return "-".join([str(year), str(month), str(date)])


pullTickerData('MSFT', formatDate(2022,5,1), formatDate(today.year, today.month, today.day))