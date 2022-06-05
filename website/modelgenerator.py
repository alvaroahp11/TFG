import yfinance as yf
import talib as tb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
import itertools

#Function that laggs dataframe
def laggDataframe(dataframeCopy, windowSize, originalDataframe):
  for window in range(1, windowSize+1):
    shifted = originalDataframe.shift(window)
    shifted.columns = [x + "-" + str(window) for x in originalDataframe.columns]
    dataframeCopy = pd.concat((dataframeCopy, shifted), axis=1)
  dataframeCopy = dataframeCopy.dropna()
  return dataframeCopy

#Function to train the mdoel
def train(Clf,config, clf_name, X_train, y_train):
    clf = Clf(**config)
    clf.fit(X_train, y_train)
    return clf

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
    X_train = df_lagged.iloc[:, 1:-1]
    y_train = df_lagged.iloc[:, 0:1]
    algoritmo = data["algorithm"][0]
    del data["stock"]
    del data["algorithm"]
    print(data)
    classifiers = ""
    if algoritmo == "RandomForestRegressor":
        classifiers = {
             algoritmo: (RandomForestRegressor, data)
        }
    elif algoritmo == "SVR":
        classifiers = {
            algoritmo: (SVR, data)
        }
    elif algoritmo == "DecisionTreeRegressor":
        classifiers = {
            algoritmo: (DecisionTreeRegressor, data)
        }
    clfFinal = ""
    for clf_name, clf_info in classifiers.items():
        Clf, hyperparams = clf_info
        hp_ks, hp_vs = hyperparams.keys(), hyperparams.values()
        configs = [dict(zip(hp_ks, v)) for v in itertools.product(*hp_vs)]
        print(config)
        for config in configs:
            clfFinal = train(Clf, config, clf_name, X_train, y_train)

    print(clfFinal)



