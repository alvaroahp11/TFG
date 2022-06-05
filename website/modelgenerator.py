import yfinance as yf
import talib as tb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

def laggDataframe(dataframeCopy, windowSize, originalDataframe):
  for window in range(1, windowSize+1):
    shifted = originalDataframe.shift(window)
    shifted.columns = [x + "-" + str(window) for x in originalDataframe.columns]
    dataframeCopy = pd.concat((dataframeCopy, shifted), axis=1)
  dataframeCopy = dataframeCopy.dropna()
  return dataframeCopy

def modelgeneration(data: dict):
    stockTicker = data["stock"]
    #Getting data
    df_data = yf.download(tickers=stockTicker, period="max", interval="1D")
    df_data.reset_index(inplace=True)

    df_data = df_data[["Date", "Close"]]

    df_data = df_data.rename(columns={"Date": "Date", "Close": "Close"})

    #Technical indicators
    df_data["EMA200"] = tb.EMA(df_data["Close"], timeperiod=200)
    df_data["EMA50"] = tb.EMA(df_data["Close"], timeperiod=50)
    df_data["RSI"] = tb.RSI(df_data["Close"], timeperiod=14)
    df_data["UP_BAND"], df_data["MID_BAND"], df_data["LOW_BAND"] = tb.BBANDS(df_data["Close"], timeperiod=20)
    df_data["MA200"] = tb.MA(df_data["Close"], timeperiod=200)
    df_data["MA50"] = tb.MA(df_data["Close"], timeperiod=50)
    df_data.dropna(inplace=True)

    #Lagg the dataframe
    df_copy = df_data.copy()
    WINDOW_SIZE = 5

    df_lagged = laggDataframe(df_copy, WINDOW_SIZE, df_data)
    df_lagged = df_lagged.drop(
        ["EMA200", "EMA50", "RSI", "UP_BAND", "MID_BAND", "LOW_BAND", "MA200", "MA50", "Date", "Date-1", "Date-2",
         "Date-3", "Date-4", "Date-5"], axis=1)

    #Data for training
    spyTrain, spyTest = train_test_split(df_lagged, test_size=0.2, random_state=1)

    X_train = spyTrain.iloc[:, 1:-1]
    y_train = spyTrain.iloc[:, 0:1]
    X_test = spyTest.iloc[:, 1:-1]
    y_test = spyTest.iloc[:, 0:1]

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)

    print(df_lagged)

