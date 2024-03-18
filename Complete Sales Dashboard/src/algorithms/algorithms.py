# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
This file is designed to contain the various Python functions used to configure tasks.

The functions will be imported by the __init__.py file in this folder.
"""

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import datetime as dt
import numpy as np
from pmdarima import auto_arima


def add_features(data):
    dates = pd.to_datetime(data["Date"])
    data["Months"] = (dates.dt.month - 6)/12
    data["Days"] = (dates.dt.isocalendar().day - 15)/30
    data["Week"] = (dates.dt.isocalendar().week - 26)/52
    data["Day of week"] = (dates.dt.dayofweek - 3.5)/7
    # Number of days after 30 December 2020
    data["Index"] = (dates - dt.datetime(2020, 12, 30)).dt.days
    return data

def preprocess(initial_data, holiday, level):
    data = initial_data.groupby(['Date'])\
                       .sum()\
                       .dropna()\
                       .reset_index()

    data['Date'] = pd.to_datetime(data['Date'])
    final_data = data[['Date','Total']]
    final_data = add_features(final_data)

    final_data['Total'] = final_data['Total']*level
    if holiday:
        final_data['Total'] *= 0.8

    date = final_data['Date'].max()
    return final_data, date

def train_arima(train_data):
    model = auto_arima(train_data['Total'],
                       start_p=1, start_q=1,
                       max_p=5, max_q=5,
                       start_P=0, seasonal=False,
                       d=1, D=1, trace=True,
                       error_action='ignore',  
                       suppress_warnings=True)
    model.fit(train_data['Total'])
    return model

def forecast(model):
    predictions = model.predict(n_periods=60)
    return np.array(predictions)

def train_xgboost(train_data):    
    y = train_data['Total']
    X = train_data.drop(['Total','Date'], axis=1)
    
    model = GradientBoostingRegressor()
    model.fit(X,y)
    return model

def forecast_xgboost(model, date):
    dates = pd.to_datetime([date + dt.timedelta(days=i)
                            for i in range(60)])
    X = add_features(pd.DataFrame({"Date":dates}))
    X.drop('Date', axis=1, inplace=True)
    predictions = model.predict(X)
    return predictions


def concat(final_data, predictions_arima, predictions_xgboost):
    date = final_data['Date'].max()

    def  _convert_predictions(final_data, predictions, date, label='Predictions'):
        dates = pd.to_datetime([date + dt.timedelta(days=i)
                                for i in range(len(predictions))])
        final_data['Date'] = pd.to_datetime(final_data['Date'])
        final_data = final_data[['Date','Total']]
        predictions = pd.concat([pd.Series(dates, name="Date"),
                                 pd.Series(predictions, name=label)], axis=1)
        return final_data.merge(predictions, on="Date", how="outer")

    result_arima = _convert_predictions(final_data, predictions_arima, date, label='ARIMA')
    result_xgboost = _convert_predictions(final_data, predictions_xgboost, date, label='Xgboost')
    return result_arima.merge(result_xgboost, on=["Date", 'Total'], how="outer").sort_values(by='Date')
