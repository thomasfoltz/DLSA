import argparse
from datetime import date
from os import path
import json
import os
import pandas as pd
import yfinance as yf

def formatDate(year, month, day):
    if month<10:
        month = "0"+str(month)
    if day<10:
        day = "0"+str(day)
    return "-".join([str(year), str(month), str(day)])

def legitDate(date):
    if len(date)!=10 or date[4]!='-' or date[7]!='-':
        return False
    if not date[0:3].isdigit() or not date[5:6].isdigit() or not date[8:9].isdigit():
        return False
    year, month, day = int(date[0:4]), int(date[6:7]), int(date[8:10])
    currYear, currMonth, currDay = today.year, today.month, today.day
    if year<1900 or year>currYear or month<1 or month>12 or day<1 or day>31:
        return False
    if (year==currYear and month>currMonth) or (day>currDay and month==currMonth and day>currDay):
        return False
    return True

def pullTickerData(ticker, startDate, currDate):
    tickerData = yf.download(ticker, startDate, currDate)
    tickerData.to_csv(os.path.join('./', r'tickerData/' + ticker + '.csv'))

def updateTickers(startDate):
    with open('stocks.json','r+') as file:
        tickers = []
        file_data = json.load(file)
        for item in file_data['holdings']:
            tickers.append(item['name'])
    if legitDate(startDate):
        for ticker in tickers:
            pullTickerData(ticker, startDate, currDate)
    else:
        print('Invalid start date')

def addStock(stock, quantity):
    stockInfo = {"name": stock,"quantity": quantity,"datePurchased": formatDate(today.year, today.month, today.day)}
    jsonFile = open("stocks.json", mode="r")
    jdata = json.load(jsonFile)
    jsonFile.close()
    jdata["holdings"].append(stockInfo)
    jsonFile = open('stocks.json', mode='w+')
    json.dump(jdata, jsonFile, indent=4)
    jsonFile.close()

def delStock(stock):
    jsonFile = open("stocks.json", mode="r")
    jdata, index = json.load(jsonFile), 0
    jsonFile.close()
    for element in jdata["holdings"]:
            if element["name"]==stock:
                del jdata["holdings"][index]
            index+=1
    jsonFile = open('stocks.json', mode='w+')
    json.dump(jdata, jsonFile, indent=4)
    jsonFile.close()

parser = argparse.ArgumentParser(description='Stock Processing Pipeline')
parser.add_argument('-a', '--add', help='stock symbol to add', type=str)
parser.add_argument('-d', '--delete', help='stock symbol to delete', type=str)
parser.add_argument('-q', '--quantity', help='quantity of stocks to add/remove', type=int, default=1)
parser.add_argument('-u', '--update', help='update all of the stocks', type=bool, default=False)
args = parser.parse_args()

today = date.today()

if args.add:
    addStock(args.add, args.quantity)
if args.delete:
    delStock(args.delete)
if args.update:
    print('Select start date for ticker history')
    year,month,day = int(input("Year: ")), int(input("Month: ")), int(input("Day: "))
    currDate = formatDate(today.year, today.month, today.day)
    startDate = formatDate(year,month,day)
    updateTickers(startDate)
