import argparse, csv, json, math, os, warnings
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from datetime import date, datetime
from random import shuffle

def formatDate(year, month, day): 
    return date(year, month, day).strftime('%Y-%m-%d')

def legitDate(date): 
    today = datetime.today().date() 
    return date.year >= 1900 and date <= today

def pullTickerData(ticker:str, startDate:str, currDate:str): 
    tickerData = yf.download(ticker, startDate, currDate) 
    tickerData.to_csv(os.path.join('./', r'static/tickerData/' + ticker + '.csv'))

def updateTickers(startDate): 
    if not legitDate(startDate): 
        print('Invalid start date') 
        return
    with open('stocks.json','r') as file:
        file_data = json.load(file)
    tickers = [item['name'] for item in file_data['holdings']]
    for ticker in tickers: pullTickerData(ticker, startDate, today)

def addStock(stock:str, quantity:int): 
    stockInfo = {"name": stock,"quantity": quantity,"datePurchased": today} 
    with open("stocks.json", mode="r") as jsonFile: 
        jdata = json.load(jsonFile) 
        jdata["holdings"].append(stockInfo) 
    with open('stocks.json', mode='w') as jsonFile: 
        json.dump(jdata, jsonFile, indent=4)

def deleteStock(stock:str): 
    with open("stocks.json", mode="r") as jsonFile: 
        jdata = json.load(jsonFile) 
        for index, element in enumerate(jdata["holdings"]): 
            if element["name"]==stock: del jdata["holdings"][index] 
            break 
        with open('stocks.json', mode='w') as jsonFile: 
            json.dump(jdata, jsonFile, indent=4)
    
    csvFile = os.path.join('static', 'tickerData', stock + '.csv')
    if os.path.exists(csvFile):
        os.remove(csvFile)

def extractTickerData(stock:str): 
    header, data = [], [] 
    with open('static/tickerData/' + stock + '.csv') as file: 
        reader = csv.reader(file) 
        header = next(reader) 
        for row in reader: data.append(row) 
    return header, data

def extractColumnData(data:list, header:str): 
    headers = {'Date':0, 'Open':1, 'High':2, 'Low':3, 'Close':4, 'Adj Close':5, 'Volume':6} 
    index = headers.get(header) 
    columnData = [row[index] for row in data] 
    if index==0: 
        columnData = [item for item in range(0, len(columnData))] 
    else: 
        columnData = [float(item) for item in columnData] 
    return columnData

def splitDataset(data:list, testRatio=0.2): 
    trainingRatio = 1 - testRatio 
    trainSize = int(trainingRatio * len(data)) 
    shuffle(data) 
    train, test = data[:trainSize], data[trainSize:] 
    return train, test

def printHoldingsData(): 
    with open('stocks.json','r+') as file: file = json.load(file) 
    for item in file['holdings']: 
        print('\n', item['name']) 
        print(extractTickerData(item['name']))

def plotData(x:list,y:list,pred,ticker:str,indep:str='Date',dep:str='Close'): 
    headers = {'Date':'Days (since earliest tracked date)', 'Open': 'Open Price ($)', 'High':'Highest Price ($)', 'Low':'Lowest Price ($)', 'Close':'Close Price ($)', 'Adj Close':'Adjusted Close Price ($)', 'Volume':'Volume of Trades'} 
    linSpace = np.linspace(min(x), max(x)) 
    ax = plt.axes() 
    ax.scatter(x, y) 
    ax.set_title('Comparison of ' + ticker + ': ' + indep + ' vs ' + dep) 
    ax.set_xlabel(headers[indep]) and ax.set_ylabel(headers[dep]) 
    plt.plot(linSpace, pred(linSpace)) 
    plt.savefig('static/plotFigures/' + ticker + '_' + indep + 'vs' + dep + '.png') 
    plt.show() and plt.close()

def polynomial(x:list,y:list,degree:int): 
    warnings.simplefilter('ignore', np.RankWarning) 
    return x, y, np.poly1d(np.polyfit(x, y, degree))

def generatePrediction(ticker:str, indep:str='Date', dep:str='Open'): 
    header, data = extractTickerData(ticker) 
    for degree in range(1,20): 
        x, y, pred = polynomial(extractColumnData(data, indep), extractColumnData(data, dep), degree) 
        err = rmse(x, y, pred) 
        if degree==1: 
            leastErr, bestPred = err, pred 
        else: 
            if err<leastErr: 
                leastErr, bestPred = err, pred 
    if args.plot: 
        plotData(x, y, bestPred, ticker, indep, dep)

def rmse(x:list, y:list, pred):
    y_pred = pred(x)
    return math.sqrt(np.square(np.subtract(y,y_pred)).mean())

if __name__ == "__main__":
    global today
    today = datetime.today().date().strftime('%Y-%m-%d')
    parser = argparse.ArgumentParser(description='Stock Processing Pipeline')
    parser.add_argument('-a', '--add', help='stock symbol to add', type=str)
    parser.add_argument('-d', '--delete', help='stock symbol to delete', type=str)
    parser.add_argument('-pl', '--plot', help='plots the best fit function', type=bool)
    parser.add_argument('-pr', '--prediction', help='compares varibles to create a best-fit polynomial', type=bool)
    parser.add_argument('-q', '--quantity', help='quantity of stocks to add/remove', type=int, default=1)
    parser.add_argument('-u', '--update', help='update all of the stocks', type=bool)
    args = parser.parse_args()

    if args.add: addStock(args.add, args.quantity)
    if args.delete: deleteStock(args.delete)
    if args.prediction:
        print('Select a holding and the independent/dependent variables to be compared')
        ticker, indep, dep= input("Ticker: "), input("Independent (default = Date): "), input("Dependent (default = Open): ")
        generatePrediction(ticker, indep, dep)
    if args.update:
        print('Select start date for ticker history')
        year, month, day = int(input("Year: ")), int(input("Month: ")), int(input("Day: "))
        today = datetime.today().date().strftime('%Y-%m-%d')
        updateTickers(date(year, month, day))