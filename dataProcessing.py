import pandas as pd
import yfinance as yf
from datetime import date
import os

def pullTickerData(ticker, start, end):
    if legitDate(start) and legitDate(end):
        tickerData = yf.download(ticker, start, end)
        tickerData.to_csv(os.path.join('./', r'tickerData/' + ticker + '.csv'))
    else:
        print("Invalid start or end date")

def formatDate(year, month, date):
    if month<10:
        month = "0"+str(month)
    if date<10:
        date = "0"+str(date)
    return "-".join([str(year), str(month), str(date)])

def legitDate(start):
    if len(start)!=10 or start[4]!='-' or start[7]!='-':
        return False
    if not start[0:3].isdigit() or not start[5:6].isdigit() or not start[8:9].isdigit():
        return False

    year, month, day = int(start[0:4]), int(start[6:7]), int(start[8:10])
    current_year, current_month, current_day = today.year, today.month, today.day

    if year<1900 or year>current_year or month<1 or month>12 or day<1 or day>31:
        return False
    if (year==current_year and month>current_month) or (day>current_day and month==current_month and day>current_day):
        return False
    return True

def updateAllTickers(tickers, start):
    if legitDate(start):
        for ticker in tickers:
            pullTickerData(ticker, start, formatDate(today.year, today.month, today.day))
    else:
        print("Invalid start date")

today = date.today()
tickers = ['MSFT', 'AAPL', 'GOOGL']
start_date = formatDate(2022, 1, 1)
updateAllTickers(tickers, start_date)

