
#importing all necessary packages
import pandas as pd
import yfinance as yf
import os

#pulling all NASDAQ traded symbols from url
df = pd.read_csv("http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt", sep='|')
csv_file = open('NASDAQ_data.csv', 'wb')
data_clean = df[df['Test Issue'] == 'N']
symbols = data_clean['NASDAQ Symbol'].tolist()
print('total number of symbols traded = {}'.format(len(symbols)))

#saving data to local csv file
df.to_csv('NASDAQ_data.csv', index=False)

