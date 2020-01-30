from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from . import app
from . import dataAccess as mydb

from flask import Flask,jsonify,render_template
from . import malipulate_database
from . import generateData_method
from . import visual_method
 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import random

#Class holding user profile after login
class User_Session:
    def __init__(self,userid,userrole, sessionid):
        self.id = userid
        self.role = userrole
        self.sessionid = sessionid

#**********************
#*****Login Page  *****
#**********************
#Entry point page for login and registration
@app.route("/",methods=['POST','GET'])
def login():
    return render_template("login.html")

#api to support login
@app.route("/api/dologin", methods=['POST'])
def dologin():
    #get required login info in json format
    data =request.get_json()
    email= data['emailLogin']
    password= data['password']
    valid_user=False
    #check valid user or not
    (valid_user,user_role,user_id,session_id) = mydb.doLogin(email,password)

    if (valid_user == True):
        #store user session

        u_sess = User_Session(user_id,user_role,session_id)
        session['user_session']=u_sess.__dict__

        #return success token to client
        res= { 'token': session_id, 'retstatus': 'login success'}
    else:
        res= { 'token': '', 'retstatus': 'login failed, invalid username or password...'}
    return res

#api to perform user registration
@app.route("/api/doregistration", methods=['POST'])
def doregistration():
    data =request.get_json() #get user info in json format
    ret = mydb.createUser(data['email'],data['fname'],data['lname'],data['password'])
    if ret == False:
        output="Registration faiiled"
    else:
        output="Registration Success"
    res= { 'retstatus': output}
    return res

#Logout page
@app.route("/Logout/")
def logout():
    session.pop('user_session',None) #clear user session and redirect to login page
    return redirect(url_for('login'))

#+++++++++++Customer+++++++++++

#**********************
#*****Profile Page  ***
#**********************

#Page for profile setting
@app.route("/Profile")
def profile():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        (email,ph_num,fname,lname,addr,post_code,city,country) = mydb.getPersonalInfo(u_sess['id'])
        (card_num,card_name,exp_mm,exp_yy,cvv) = mydb.getCardInfo(u_sess['id'])
        user_prof= {'email':email,'ph_num':ph_num,'fname':fname,'lname':lname,'addr':addr,'post_code':post_code,'city':city,'country':country}
        card_info= {'card_num':card_num,'card_name':card_name,'exp_mm':exp_mm,'exp_yy':exp_yy,'cvv':cvv}
        return render_template("profile.html",userprof=user_prof,cardinfo=card_info) #return profile template
    else:
        return redirect(url_for('login')) #redirect to login page if user session not found

#api for handling profile update
@app.route("/api/updateprofile", methods=['POST'])
def updateprofile():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session'] #get back user session containing user information
        data =request.get_json() #get update info. from client in json format
        #perform update
        ret = mydb.updatePersonalInfo(u_sess['id'],data['email'],data['phone'],data['fname'],data['lname'],data['address'],data['pincode'],data['city'],data['country'])
        if ret == True:
            output = "Update Success"
        else:
            output = "Update Failed"
        res= { 'retstatus': output} #tell client if success or not
        return res
    else:
        return None

#api for handling card info update
@app.route("/api/updatecardinfo", methods=['POST'])
def updatecardinfo():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session'] #get back user session containing user information
        data =request.get_json() #get update info. from client in json format
        #perform card update
        ret = mydb.updateCardInfo(u_sess['id'],data['cnum'],data['cname'],data['exp_mm'],data['exp_yy'],data['cvv'])
        if ret == True:
            output = "Update Success"
        else:
            output = "Update Failed"
        res= { 'retstatus': output} #tell client if success or not
        return res
    else:
        return None

#api for handling close account
@app.route("/api/closeuseraccount", methods=['POST'])
def closeuseraccount():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session'] #get back user session containing user information
        data =request.get_json() #get update info. from client in json format
        #close account
        ret = mydb.deactivateUser(u_sess['id'],data['ca_email'])
        if ret == 0:
            output="Email mismatching, unable to close account"
        else:
            output="Account Closed Successfully"
        res= { 'retstatus': output}
        return res
    else:
        return None

#**********************
#*****Rent Page    ****
#**********************
#Page for rent, including function on bike rent, return and defect reporting
@app.route("/Rent", methods=['POST','GET'])
def rent():
    (tkbike_id, tkbike_loc) = mydb.trackbikes(True) #get all bikes (not in used) location 
    stat= mydb.getBikeStations() #get bike station id and name
    if request.method=='POST': #on rent or return bike click, browser will post back for update latest bike count
        orderid=request.form['orderid']
        bikeid=request.form['bikeid']

        if 'user_session' in session: #check user login before or not
            #with order id and bike id from rent or return that need to display to user for a rent session
            return render_template("rent.html",tkbikeid=tkbike_id, tkbikeloc=tkbike_loc,orderid=orderid,bikeid=bikeid,stat=stat)
        else:
            return redirect(url_for('login')) #user did not login before
    else: 
        if 'user_session' in session: #check user login before or not
            #render page without order id and bike id, not in rent session
            return render_template("rent.html",tkbikeid=tkbike_id, tkbikeloc=tkbike_loc,orderid='',bikeid='',stat=stat)
        else:
            return redirect(url_for('login')) #user did not login before

#api to handle defect reported
@app.route("/api/report_defect", methods=['POST'])
def report_defect():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        data =request.get_json() #get defect details in json format
        #create a new defect report
        ret = mydb.createDefectReport(u_sess['id'],data['bike_id'],data['def_category'],data['def_details'])
        if ret== True:
            #update bike status to defect
            ret = mydb.updateBikeState(data['bike_id'],'D')
        if ret == False:
            output="Defect Report failed"
        else:
            output="Defect Report Success"
        res= { 'retstatus': output}
        return res
    else:
        return None

#api to handle bike renting
@app.route("/api/rent_bike", methods=['POST'])
def rent_bike():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        data =request.get_json() #get bike id to be rent
        (ret, orderid) = mydb.createOrder(u_sess['id'],data['bike_id']) #create a new order
        ret = mydb.updateBikeState(data['bike_id'],'U') #bike marked in use
        if ret == False:
            output="Rent failed"
        else:
            output="Rent Success"
        res= { 'retstatus': output, 'orderid': orderid} #return order id created
        return res
    else:
        return None

#api to handle bike return
@app.route("/api/return_bike", methods=['POST'])
def return_bike():
    if 'user_session' in session: #check user session exist or not
        data =request.get_json()
        (ret, amount, duration) = mydb.settleOrder(data["order_id"]) #settle order with amount and duration calculated
        ret = mydb.updateBikeState(data['bike_id'],'A',data['station_id']) #mark bike available
        if ret == False:
            output="Return failed"
        else:
            output="Return Success"
        res= { 'retstatus': output, 'amount': str(amount)+" pounds", 'duration':duration} #return amount and duration
        return res
    else:
        return None

#**********************
#*****Home Page    ****
#**********************

#Page for introduction, displayed after customer login successfully
@app.route("/Home")
def home():
    if 'user_session' in session: #check user login before or not
        user_role = session['user_session']['role']
        if user_role== 1:
            return render_template("index.html")
        elif user_role== 2:
            return redirect(url_for('adminIndex'))
        elif user_role == 3:
            return redirect(url_for('showmanagerHome'))
        else:
            return redirect(url_for('logout'))
         
    else:
        return redirect(url_for('login'))


#+++++++++++Operator+++++++++++

#**********************
#*****Operation page***
#**********************
#Operator page for tracking bikes, manage defects, moving bikes
#with Dashboard to show summary in one page
@app.route("/admin",methods=['POST','GET'])
def adminIndex():

    if 'user_session' in session: #check user session exist or not
        dashboard= mydb.getDashBoardFig() #get figures for dashboard
        (tkbike_id, tkbike_loc) = mydb.trackbikes() #get bikes location
        (df_rpt) = mydb.showDefectReport() #get defect reports
        (parking_status)= mydb.showBikeStations() #get bike stations occupying rate
        lststation= list(parking_status['station_id'])
        lstrate= list(parking_status['occ_rate'])
        lstcolor= [] #different color depending on occupying rate

        for i in range(0,len(lstrate)):
            if lstrate[i] >= 80: #RED in case of over 80%
                lstcolor.append("rgba(216,56,7,1)")
            elif lstrate[i] <=20: #YELLO in case of less than 20%
                lstcolor.append("rgba(244,233,76,1)")
            else:
                lstcolor.append("rgba(2,117,216,1)")
        #render page with live content retreive from database
        return render_template("/admin/index.html", dfig=dashboard, tkbikeid=tkbike_id, tkbikeloc=tkbike_loc, dfrpt=df_rpt, parkid=lststation, parkrate=lstrate, parkcolor=lstcolor)
    else:
        return redirect(url_for('login'))

#api for changing defect report status, for managing defect
#RD-new defect-->RI-investigating-->RF-fixed
@app.route("/api/changeDefectStatus", methods=['POST'])
def changeDfStatus():
    if request.method == "POST":
        data =request.get_json()
    id= data['id'] #get status in json format, id and new status
    newdfStatus= data['newdfStatus']
    ok = mydb.updateDefectStatus(id,newdfStatus) #perform update
    
    if (ok == True): #return result
        res= { 'result': 'ok'} 
    else:
        res= { 'result': 'nok'}
    return res

#dummy page RFU
@app.route("/blank",methods=['POST','GET'])
def blankPage():
    return render_template("/admin/blank.html")

#+++++++++++Operator+++++++++++
#**********************
#*****Manager page***
#**********************


#extract data from database or csv file.
def querydatabase(end):
    #1. method to use data base 
    # database = 'bikehistoryall.db'
    # db = connet_datebase(database)
    # sql_query = 'SELECT * FROM alldata'
    # df = pd.read_sql(sql_query, con=db)
    # db.commit()
    # db.close()
    #
    #2. original dataset
    original_data = pd.read_csv('train.csv')# train.csv for real bike reting dataset from kaggle.com
    #end = random.randint(0,10000)# we can choose rows randomly
    df = original_data.loc[:end]
    return df

#method for count all order in a year. It process data query from database or csv file.
def countall_hours(df):
    #create dataframe for counting total bike using count_all
    #row is 24 hours in a day
    count_all = pd.DataFrame({'Time': np.arange(0, 24, 1), 'Count': [0] * 24})
    #count from original dataset
    for i in range(df.shape[0]):
        time = int(df.loc[i, 'datetime'][11:13])
        count_all.iloc[time, 1] += int(df.loc[i, 'count'])
    #extract from dataframe
    startDate = df.iloc[0, 0][0:10]
    endDate = df.iloc[df.shape[0] - 1, 0][0:10]
    x = np.arange(0, 24, 1)
    y = count_all['Count']
    return x,y,startDate,endDate

#method for count all order in a year. It process data query from database or csv file.
def countall_year():
    #to choose extract how many data from database or file
    df1 = querydatabase(2000)
    df2 = querydatabase(3000)
    #count total use situation
    count_all1 = pd.DataFrame({'Month': np.arange(0, 12, 1), 'Count': [0] * 12})
    count_all2 = pd.DataFrame({'Month': np.arange(0, 12, 1), 'Count': [0] * 12})

    #add each line count to count_all1
    for i in range(df1.shape[0]):
        month = int(df1.loc[i, 'datetime'][5:7])
        count_all1.iloc[month-1, 1] += int(df1.loc[i, 'count'])
    for i in range(df2.shape[0]):
        month = int(df2.loc[i, 'datetime'][5:7])
        count_all2.iloc[month-1, 1] += int(df2.loc[i, 'count'])

    #extract only month from datatime
    startDate1 = df1.iloc[0, 0][0:10]
    endDate1 = df1.iloc[df1.shape[0] - 1, 0][0:10]
    startDate2 = df2.iloc[0, 0][0:10]
    endDate2 = df2.iloc[df2.shape[0] - 1, 0][0:10]

    #return each comlun individually
    x1 = count_all1['Month']
    y1 = count_all1['Count']
    x2 = count_all2['Month']
    y2 = count_all2['Count']

    return x1,y1,startDate1,endDate1,x2,y2,startDate2,endDate2

# render index page for manager & also page for user to select date period and download custome report
@app.route('/manager')
def showmanagerHome():
    return render_template('manager/defectinfo.html')

#use for produce report
@app.route('/manager/producereport', methods=['POST', 'GET'])
def produecereport():
    print('ative drawing')
    req = request.get_json()
    word = str(req['megs'])
    startTime = str(req['startTime'])
    endTime = str(req['endTime'])
    startTime1 = req['startTime1']
    endTime1 = str(req['endTime1'])
    startTime2 = str(req['startTime2'])
    endTime2 = str(req['endTime2'])
    startTime3 = str(req['startTime3'])
    endTime3 = str(req['endTime3'])
    startTime4 = str(req['startTime4'])
    endTime4 = str(req['endTime4'])
    startTime5 = str(req['startTime5'])
    endTime5 = str(req['endTime5'])
    # print(word)
    # print(startTime)
    # print(endTime)
    #Visual.produceReport(startTime,endTime,startTime1,endTime1,startTime2,endTime2,startTime3,endTime3,startTime4,endTime4,startTime5,endTime5,word)
    Visual.produceReport()
    #np.savetxt('test.txt',startTime)
    # print("Downloading File")
    #send_file("/report.jpeg", as_attachment=True)
    if not req:
        return jsonify({'error': 'Missing data!'})


    return redirect(url_for('showmanagerHome'))

#render defectinfo page
@app.route('/defectinfo')
def showdefectinfo():
    return render_template('manager/defectinfo.html')


#render showshowTotalCounts/24H page
@app.route('/showTotalCounts/24H')
def showTotalCounts24H():
    #choose dateaframe to query
    df = querydatabase(200)
    x,y,startDate,endDate  = countall_hours(df)
    x = list(x)
    y = list(y)
    return render_template('manager/showTotalCounts24H.html', x=x, y=y)

#render showTotalCounts/year page
@app.route('/showTotalCounts/year')
def showTotalCountsYear():
    #get processed data from countall_yaer
    x1,y1,startDate1,endDate1,x2,y2,startDate2,endDate2 = countall_year()
    x1 = list(x1)
    y1 = list(y1)
    x2 = list(x2)
    y2 = list(y2)
    return render_template('manager/showTotalCountsYear.html', x1=x1, y1=y1, x2=x2, y2=y2)
