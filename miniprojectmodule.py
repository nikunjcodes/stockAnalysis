# -*- coding: utf-8 -*-
"""miniprojectmodule.ipynb

"""
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def getbasic(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_name = soup.find("h1", class_="D(ib) Fz(18px)").text.strip()
        stock_price = soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text.strip()
        stock_info = soup.find("div", class_="C($tertiaryColor) Fz(12px)").text.strip()

        print(f"Stock Name: {stock_name}")
        print(f"Stock Price: {stock_price}")
        print(f"Stock Info: {stock_info}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
def get_more_info(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        market_cap = soup.find('td', class_='Ta(end) Fw(600) Lh(14px)', attrs={'data-test': 'MARKET_CAP-value'}).text.strip()
        pe_ratio = soup.find("td",class_="Ta(end) Fw(600) Lh(14px)",attrs={'data-test':"PE_RATIO-value"}).text.strip()
        eps = soup.find("td", class_="Ta(end) Fw(600) Lh(14px)",attrs={'data-test':"EPS_RATIO-value"}).text.strip()
        print(f"Market Cap: {market_cap}")
        print(f"Price to Earnings ration: {pe_ratio}")
        print(f"EPS : {eps}")

def plot_historical_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    ath_index = stock_data['Close'].idxmax()
    atl_index = stock_data['Close'].idxmin()
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price')
    plt.scatter(ath_index, stock_data['Close'].loc[ath_index], color='red', label='All-Time High')
    plt.scatter(atl_index, stock_data['Close'].loc[atl_index], color='green', label='All-Time Low')
    plt.title(f'{ticker} Historical Stock Data (All time)')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (RS)')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_onemonth_data(ticker):
    stock_data = yf.download(ticker, start='2023-11-02', end='2023-12-02')
    ath_index = stock_data['Close'].idxmax()
    atl_index = stock_data['Close'].idxmin()
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price')
    plt.scatter(ath_index, stock_data['Close'].loc[ath_index], color='red', label='Monthly-Time High')
    plt.scatter(atl_index, stock_data['Close'].loc[atl_index], color='green', label='Monthly-Time Low')
    plt.title(f'{ticker} Historical Stock Data (Past month  )')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')  # Update with the appropriate currency if needed
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_oneyear_data(ticker):
    stock_data = yf.download(ticker, start='2022-12-02', end='2023-12-02')
    ath_index = stock_data['Close'].idxmax()
    atl_index = stock_data['Close'].idxmin()
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price')
    plt.scatter(ath_index, stock_data['Close'].loc[ath_index], color='red', label='YTD High')
    plt.scatter(atl_index, stock_data['Close'].loc[atl_index], color='green', label='YTD Low')
    plt.title(f'{ticker} Historical Stock Data (Past year)')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')  # Update with the appropriate currency if needed
    plt.legend()
    plt.grid(True)
    plt.show()


def get_balance_sheet(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}"
    header = {'Connection': 'keep-alive',
                'Expires': '-1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                }
    r = requests.get(url, headers=header)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find_all('div', attrs={'class': 'D(tbhg)'})
    if len(div) < 1:
        print("Fail to retrieve table column header")
        exit(0)
    col = []
    for h in div[0].find_all('span'):
        text = h.get_text()
        if text != "Breakdown":
            col.append( datetime.strptime(text, "%m/%d/%Y") )
    df = pd.DataFrame(columns=col)
    for div in soup.find_all('div', attrs={'data-test': 'fin-row'}):
        i = 0
        idx = ""
        val = []
        for h in div.find_all('span'):
            if i == 0:
                idx = h.get_text()
            else:
                num = int(h.get_text().replace(",", ""))/1000000000
                val.append( num )
            i += 1
        row = pd.DataFrame([val], columns=col, index=[idx] )
        df = df._append(row)
    return df
def balance(stock_symbol):
    return (get_balance_sheet(stock_symbol))

def visualize_balance_sheet(ticker):
    df = get_balance_sheet(ticker)
    df.plot(kind='bar', figsize=(10, 6), colormap='viridis')
    plt.title('Financial Data Visualization')
    plt.xlabel('Categories')
    plt.ylabel('Values(in Tr')
    plt.show()

def get_analyst_recommendations(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_rating = soup.find("div",
                                   class_="B(8px) Pos(a) C(white) Py(2px) Px(0) Ta(c) Bdrs(3px) Trstf(eio) Trsde(0.5) Arrow South Bdtc(i)::a Fw(b) Bgc($buy) Bdtc($buy)",
                                   attrs={'data-test': 'rec-rating-txt'})
        print(f"{stock_symbol} has a rating of {stock_rating}")
        if(stock_rating<2):
            print("Strong Buy Rating !!!")
        elif(stock_rating>2 and stock_rating<3):
            print("Buy Rating")
        elif(stock_rating>3 and stock_rating<4):
            print("Underperform rating")
        else:
            print("Sell now !!!")

