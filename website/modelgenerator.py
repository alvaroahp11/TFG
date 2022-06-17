import datetime

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

def parseData(data: dict, algoritmo):
    if algoritmo == "RandomForestRegressor":
        data["n_estimators"][0] = int(data["n_estimators"][0])
        if data["max_depth"][0] == "None":
            data["max_depth"][0] = None
        else:
            data["max_depth"][0] = int(data["max_depth"][0])

        data["min_samples_split"][0] = int(data["min_samples_split"][0])
        data["min_samples_leaf"][0] = int(data["min_samples_leaf"][0])

    elif algoritmo == "SVR":
        data['degree'][0] = int(data['degree'][0])

    elif algoritmo == "DecisionTreeRegressor":
        if data["max_depth"][0] == "None":
            data["max_depth"][0] = None
        else:
            data["max_depth"][0] = int(data["max_depth"][0])
        data["min_samples_split"][0] = int(data["min_samples_split"][0])
        data["min_samples_leaf"][0] = int(data["min_samples_leaf"][0])

def technicalIndicators(df):
    dfCopy = df.copy()
    dfCopy["EMA200"] = tb.EMA(dfCopy["Close"], timeperiod=200)
    dfCopy["EMA50"] = tb.EMA(dfCopy["Close"], timeperiod=50)
    dfCopy["RSI"] = tb.RSI(dfCopy["Close"], timeperiod=14)
    dfCopy["UP_BAND"], dfCopy["MID_BAND"], dfCopy["LOW_BAND"] = tb.BBANDS(dfCopy["Close"], timeperiod=20)
    dfCopy["MA200"] = tb.MA(dfCopy["Close"], timeperiod=200)
    dfCopy["MA50"] = tb.MA(dfCopy["Close"], timeperiod=50)
    dfCopy.dropna(inplace=True)
    return dfCopy

def modelgeneration(data: dict):
    stockTicker = data["stock"]
    #Getting data
    df_data = yf.download(tickers=stockTicker, period="max", interval="1D")
    df_data.reset_index(inplace=True)

    crudeData = df_data[["Date", "Close"]]

    df_data = crudeData.rename(columns={"Date": "Date", "Close": "Close"})

    #Technical indicators
    df_data = technicalIndicators(df_data)

    #Lagg the dataframe
    df_copy = df_data.copy()
    WINDOW_SIZE = 5

    df_lagged = laggDataframe(df_copy, WINDOW_SIZE, df_data)
    df_lagged = df_lagged.drop(
        ["EMA200", "EMA50", "RSI", "UP_BAND", "MID_BAND", "LOW_BAND", "MA200", "MA50", "Date", "Date-1", "Date-2",
         "Date-3", "Date-4", "Date-5"], axis=1)

    #Data for training
    X_train = df_lagged.iloc[:, 1:]
    y_train = df_lagged.iloc[:, 0:1]
    algoritmo = data["algorithm"][0]
    del data["stock"]
    del data["algorithm"]
    parseData(data, algoritmo)
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
        for config in configs:
            clfFinal = train(Clf, config, clf_name, X_train, y_train)


    oldData = crudeData.tail(20)
    dictOldData = {}
    for index, row in oldData.iterrows():
        dictOldData[str(row['Date'].date())] = row['Close']

    finalPrediction = {}
    for i in range(20):
        #lagg the dataframe
        df_data = technicalIndicators(crudeData)
        df_copy = df_data.copy()
        WINDOW_SIZE = 4
        df_lagged = laggDataframe(df_copy, WINDOW_SIZE, df_data)
        df_lagged = df_lagged.drop(["Date", "Date-1", "Date-2", "Date-3", "Date-4"], axis=1)
        df_lagged = df_lagged.iloc[-1].array
        df_lagged = df_lagged.reshape(1, -1)
        prediction = clfFinal.predict(df_lagged)
        dayPlusOne = crudeData.iloc[-1]["Date"] + pd.DateOffset(1)
        finalPrediction[str(dayPlusOne.date())] = prediction[0]
        crudeData.loc[len(crudeData.index)] = [dayPlusOne, prediction[0]]
        if i == 0:
            dictOldData[str(dayPlusOne.date())] = prediction[0]

    return finalPrediction, dictOldData









