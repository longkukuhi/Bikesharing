#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,jsonify,render_template
from malipulate_database import *
from generateData_method import *
from visual_method import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import random
 
app = Flask(__name__)#instance
 
testInfo = {}

@app.route('/test_post/nn',methods=['GET','POST'])#路由
def test_post():
    rows = querydatabase()
    testInfo['name'] = rows[0][0]
    testInfo['age'] = rows[1][0]
    return json.dumps(testInfo)

def querydatabase(end):
    # database = 'bikehistoryall.db'
    # db = connet_datebase(database)
    # sql_query = 'SELECT * FROM alldata'
    # df = pd.read_sql(sql_query, con=db)
    # db.commit()
    # db.close()
    original_data = pd.read_csv('train.csv')
    #end = random.randint(0,10000)
    df = original_data.loc[:end]
    return df


def countall_hours(df):
    count_all = pd.DataFrame({'Time': np.arange(0, 24, 1), 'Count': [0] * 24})
    for i in range(df.shape[0]):
        time = int(df.loc[i, 'datetime'][11:13])
        count_all.iloc[time, 1] += int(df.loc[i, 'count'])

    startDate = df.iloc[0, 0][0:10]
    endDate = df.iloc[df.shape[0] - 1, 0][0:10]
    x = np.arange(0, 24, 1)
    y = count_all['Count']
    return x,y,startDate,endDate

def countall_year():
    df1 = querydatabase(4000)
    df2 = querydatabase(50000)
    count_all1 = pd.DataFrame({'Month': np.arange(0, 12, 1), 'Count': [0] * 12})
    count_all2 = pd.DataFrame({'Month': np.arange(0, 12, 1), 'Count': [0] * 12})
    for i in range(df1.shape[0]):
        month = int(df1.loc[i, 'datetime'][5:7])
        count_all1.iloc[month-1, 1] += int(df1.loc[i, 'count'])
    for i in range(df2.shape[0]):
        month = int(df2.loc[i, 'datetime'][5:7])
        count_all2.iloc[month-1, 1] += int(df2.loc[i, 'count'])

    startDate1 = df1.iloc[0, 0][0:10]
    endDate1 = df1.iloc[df1.shape[0] - 1, 0][0:10]
    startDate2 = df2.iloc[0, 0][0:10]
    endDate2 = df2.iloc[df2.shape[0] - 1, 0][0:10]

    x1 = count_all1['Month']
    y1 = count_all1['Count']
    x2 = count_all2['Month']
    y2 = count_all2['Count']

    return x1,y1,startDate1,endDate1,x2,y2,startDate2,endDate2


@app.route('/defectinfo')
def showdefectinfo():
    return render_template('defectinfo.html')

@app.route('/download')
def downloadReport():
    return render_template('manager.html')


@app.route('/showTotalCounts/24H')
def showTotalCounts24H():
    df = querydatabase(500)
    x,y,startDate,endDate  = countall_hours(df)
    x = list(x)
    y = list(y)
    return render_template('showTotalCounts24H.html',x=x,y=y)


@app.route('/showTotalCounts/year')
def showTotalCountsYear():
    x1,y1,startDate1,endDate1,x2,y2,startDate2,endDate2 = countall_year()
    x1 = list(x1)
    y1 = list(y1)
    x2 = list(x2)
    y2 = list(y2)
    return render_template('showTotalCountsYear.html',x1=x1,y1=y1,x2=x2,y2=y2)


@app.route('/')
def hello_world():
    return 'Welcome! Manager!'
 
@app.route('/index')
def index():
    return render_template('index.html')
 

