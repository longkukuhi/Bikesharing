import sqlite3
from . import app  
from flask import g
import numpy as np
import pandas as pd
import time, datetime
from hashlib import sha1

#variable contains db for system used
PRJ_DB = "bikeRenting.db"
RATE = 10.0 #pounds per min.

#db connection stored and shared within request context
def get_db():
    db=getattr(g,"_bikedb",None)
    if db is None:
        db= g._bikedb= sqlite3.connect(PRJ_DB)
    return db
#release connection resource after request context
@app.teardown_appcontext
def close_connection(exception):
    db=getattr(g,'_bikedb',None)
    if db is not None:
        db.close

#**********************
#*****Login Page  *****
#**********************

#create user account
def createUser(email,fname,lname,password):
    try:

        # Hashing passwords
        salt = "5gz"
        password = password+salt
        hashedPassword = sha1(password.encode("utf-8")).hexdigest()

        user_role = 1# default customer role

        #user create date time
        timestamp = time.localtime(time.time())
        current_date = time.strftime('%Y-%m-%d %H:%M', timestamp)

        cur= get_db().cursor()
        #create user profile
        cur.execute("""INSERT INTO users (email,first_name,last_name,password,role_id,create_date)
         VALUES (?,?,?,?,?,?)""", (email,fname,lname,hashedPassword,user_role,current_date))
        get_db().commit()
        return True
    except:
        print("createUser error")
        get_db().rollback()
        return False

#update user password RFU
#present valid old password before update or
#isreset is true, no need to present old password
def updateUserPassword(email,oldpassword,newpassword,isreset=False):
    return True

#Login, return user role, user id and session no. after valid password check
def doLogin(email,password):
    try:
        # Creating hash
        salt = "5gz"
        password = password+salt
        hashedPass = sha1(password.encode("utf-8")).hexdigest() #recover hashed password

        cur= get_db().cursor()
        #get user info by presenting email and password as credential
        cur.execute("SELECT role_id, user_id, isActive, password FROM users WHERE email = ?", [email])
        row= cur.fetchone()
        role_id= row[0]
        user_id= row[1]
        isActive= row[2] #check if the account has been closed 1, active, 0 inactive
        secret= row[3]
        if hashedPass == secret and isActive == 1: #login success while passord correct and acct. active
            session_ran = np.random.randint(0,10,7)
            session_no=""
            for unit in session_ran: #create session no. for identify user session
                session_no= session_no + str(unit)
            return (True, role_id, user_id, session_no)
        else:
            return (False,-1,'','')
    except:
        print("doLogin error")
        return (False,-1,'','') 

#+++++++++++Customer+++++++++++

#**********************
#*****Profile Page  ***
#**********************

# get user profile, with initial info. from registration
def getPersonalInfo(user_id):
    try:
        cur = get_db().cursor()
        #retrieve profile from database
        cur.execute(
        "SELECT email, phone_number, first_name, last_name, address, post_code, city, country FROM users where user_id = ?", [user_id])
        result = cur.fetchone()
        email = result[0]
        phone_number = result[1]
        first_name = result[2]
        last_name = result[3]
        address = result[4]
        post_code = result[5]
        city = result[6]
        country = result[7]
        return (email,phone_number,first_name,last_name,address,post_code,city,country) #return required fields
    except:
        print("Fail to read personal info")
        raise

# Update the personal profile
def updatePersonalInfo(user_id,email,phone_number,first_name,last_name,address,post_code,city,country):
    try:
        cur = get_db().cursor()
        #update profile
        cur.execute(
        "UPDATE users SET email = ?, phone_number = ?, first_name = ?, last_name = ?, address = ?, post_code = ?, city = ?, country = ?  where user_id = ?", (
        email, phone_number, first_name, last_name, address, post_code, city, country, user_id))
        get_db().commit()
        return True
    except:
        print("Fail to update personal info")
        return False

# Close user account by setting isActive flag to 0
def deactivateUser(user_id,email):
    try:
        cur = get_db().cursor() 
        #set isActive flag to 0 to close account, logical delete only, pending for house keeping to del. record
        cur.execute(
        "UPDATE users SET isActive = 0 WHERE user_id = ? AND email = ?", (
        user_id, email))
        get_db().commit()
        if  cur.rowcount == 1: #record found and update performed
            return 1
        else:
            return 0
    except:
        print("Fail to deactivateUser")
        raise


# Update payment card info, insert new record if no card info found for corresponding user
def updateCardInfo(user_id,card_num,card_name,exp_mm,exp_yy,cvv):
    try:
        cur = get_db().cursor()
        cur.execute(
        "SELECT COUNT(*) FROM accounts where user_id = ?", [user_id]) #check for user account exist
        result = cur.fetchone()       
        if result[0] == 0: #insert
            cur.execute(
                "INSERT INTO accounts (user_id, card_number, card_holder, exp_mm, exp_yy, cvv_digits) VALUES (?,?,?,?,?,?)", (
                user_id, card_num, card_name, exp_mm, exp_yy, cvv))
            get_db().commit()
            return True

        elif result[0] == 1: #update
            cur.execute(
                "UPDATE accounts SET card_number = ?, card_holder = ?, exp_mm = ?, exp_yy = ?, cvv_digits = ? WHERE user_id = ?", (
                card_num, card_name, exp_mm, exp_yy, cvv, user_id))
            get_db().commit()
            return True
        else:
            return False
    except:
        print("Fail to update card info")
        return False


# Get default card info.
def getCardInfo(user_id):
    try:
        cur = get_db().cursor()
        #get info. from database
        cur.execute("SELECT card_number,card_holder,exp_mm,exp_yy,cvv_digits FROM accounts WHERE user_id = ?", [user_id])
        result = cur.fetchone()
        if result == None:
            card_num = ""
            card_name = ""
            exp_mm = ""
            exp_yy = ""
            cvv = ""                
        else:   
            card_num = result[0]
            card_name = result[1]
            exp_mm = result[2]
            exp_yy = result[3]
            cvv = result[4]        
        return card_num, card_name, exp_mm, exp_yy, cvv #return info
    except:
        print("Fail to get Card Info")
        raise


#**********************
#*****Rent Page    ****
#**********************

#Create Defect incident
#Status RD-reported new defect, RI-reported investigating, RF-reported fixed
def createDefectReport(user_id,bike_id,category,details):
    try:
        cur = get_db().cursor()
        timestamp = time.localtime(time.time()) #get current date time
        report_datetime = time.strftime('%Y-%m-%d %H:%M', timestamp)
        status = "RD"  # default
        cur.execute(
            "INSERT INTO defect_report (user_id,bike_id,category,details,report_datetime,status) VALUES (?,?,?,?,?,?)",
            (user_id, bike_id, category, details, report_datetime, status))
        get_db().commit()
        return True
    except:
        print("Fail to create defect report")
        return False

#Create order releted to rent action, return order_id
def createOrder(user_id,bike_id):
    try:
        cur = get_db().cursor()
        timestamp = time.localtime(time.time()) #get current date time
        start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
        #create new order
        cur.execute("INSERT INTO orders (user_id, bike_id, start_datetime) VALUES (?, ?, ?)",(user_id, bike_id,start_datetime))
        get_db().commit()
        #get order id which is auto. increment
        cur.execute("SELECT last_insert_rowid()")
        result = cur.fetchone()
        return (True, result[0])
    except:
        print("Fail to create order!")
        return (False, -1)

#Update order releted to return action, to complete a order transaction
def settleOrder(order_id):
    try:
        cur = get_db().cursor()
        #get back to rent start date time from database for payment calculation
        cur.execute("SELECT start_datetime FROM orders WHERE order_id = ?", [order_id])
        str_start_datetime = str(cur.fetchone()[0])
        #get current date time as termination
        str_end_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #change back to datetime object
        start_datetime= datetime.datetime.strptime(str_start_datetime,'%Y-%m-%d %H:%M:%S')
        end_datetime= datetime.datetime.strptime(str_end_datetime,'%Y-%m-%d %H:%M:%S')
        delta= end_datetime - start_datetime #duration calculation
        duration = round(delta.seconds/60,2)
        amount = round(duration * RATE,2) #payment ammount calculation
        #settle order 
        cur.execute("UPDATE orders SET end_datetime = ?,amount = ? WHERE order_id = ?", (str_end_datetime,amount,order_id))
        get_db().commit()
        return True, amount, duration
    except:
        print("Fail to settle Order")
        return False, 0
    return True

#Update bike location and bike status U-Using,A-Available,D-Defect
#can be called by from Bike GPS System, which update location in regular based e.g. minutes (not in this project scope)
def updateBikeState(bike_id, status, park_loc_id=1, lat=-1, long=-1):
    try:
        cur = get_db().cursor()
        if status == 'A': #for bike return, mark available & parking location
            cur.execute("UPDATE bikes SET parked_bike_station=?, status=? WHERE bike_id =?", (park_loc_id, status, bike_id))
        elif status == 'D': #for bike reported with defect
            cur.execute("UPDATE bikes SET status=? WHERE bike_id =?", (status, bike_id))       
        elif status == 'U': #for bike rent, mark in using status
            cur.execute("UPDATE bikes SET status=? WHERE bike_id =?", (status, bike_id))
        else: #for bike location system to update different bikes' location in regular time based
            cur.execute("UPDATE bikes SET loc_lat=?, loc_long=? WHERE bike_id =?", (lat, long, status, bike_id))
        get_db().commit()
        return True
    except:
        print("Fail to update bike")
        return False

#get bike station information e.g. id and name
def getBikeStations():
    try:
        result={} #will contain result set in id and name pair
        cur = get_db().cursor()
        cur.execute("SELECT station_id, name FROM bike_stations") #get all station info from db
        for row in cur.fetchall():
            result[row[0]]=row[1]
              
        return result
    except:
        print("Fail to get Bike station Info")
        raise

#+++++++++++Operator+++++++++++

#**********************
#*****Track bikes  ****
#**********************

#Return list of bikes with loc. info and status
#excludeused set true if only include avaliable bikes in the list
def trackbikes(excludeused=False):
    try:
        bikeid= [] #bike list
        locs=[]
        cur= get_db().cursor()
        if excludeused == True: #exclude used bikes
            cur.execute("SELECT bike_id, loc_lat, loc_long FROM bikes WHERE status = 'A'")
        else: #include all bikes
            cur.execute("SELECT bike_id, loc_lat, loc_long FROM bikes")
        for row in cur.fetchall(): #create bike list
            bikeid.append(row[0])
            locs.append({'lat': row[1] , 'lng': row[2] })

        return (bikeid,locs) #return list wit id and location
    except:
        print("trackbikes error")
        return None

#Show dash board, return different bike status counts and no. of open defects in defect report
def getDashBoardFig():
    try:
        results= {}
        cur= get_db().cursor()
        cur.execute("SELECT status, count(*) FROM bikes GROUP BY status") #diffect count on bike diff. status
        for row in cur.fetchall():
            results[row[0]]= row[1]

        cur.execute("SELECT count(*) from defect_report WHERE status <> 'DF'") #no. of outstanding defect
        count= cur.fetchone()
        results['T']=count[0]

        return results
    except:
        print("showDashBoardFig error")
        return None 

#Show outstanding defects
def showDefectReport():
    try:
        cur= get_db().cursor() #get content on defect reports
        cur.execute("""SELECT D.report_id, U.email, D.bike_id, D.category, 
        D.details, D.report_datetime, D.status FROM defect_report D, 
        users U on D.user_id = U.user_id where status <> 'DF'""")
        rows=  cur.fetchall()

        return (rows)
    except:
        print("showDefectReport error")
        return None

#Change defect status
#Status as RD-reported defect, RI-reported investigating, RF-reported fixed
def updateDefectStatus(id, new_status):
    try:
        cur= get_db().cursor() #update status
        cur.execute("UPDATE defect_report SET status=? where report_id = ?", (new_status, id))
        get_db().commit()
        return True
    except:
        print("updateDefectStatus")
        get_db().rollback()
        return False

#Show bikes that require move action, bikes station lack of bike or overcrowded
def showBikeStations():
    try:

        #get no. of bikes that not in used e.g. packed@bike station
        sql1="""SELECT count(*) as 'num_bikes', parked_bike_station FROM bikes WHERE status <> 'U' 
        GROUP BY parked_bike_station"""
        #get different bike station location and capacity
        sql2="SElECT station_id, post_code, loc_lat, loc_long, bike_rack_number FROM bike_stations"
        bikescountfrm= pd.read_sql_query(sql1,get_db())
        stationfrm= pd.read_sql_query(sql2,get_db())
        #calculate rate of occupying e.g. no. of bikes parked/station capacity
        resultset= pd.merge(stationfrm,bikescountfrm,how='outer',left_on='station_id',right_on='parked_bike_station')
        resultset['occ_rate']=round(resultset['num_bikes']/resultset['bike_rack_number']*100,2)
        return (resultset)
    except:
        print("showBikeStations error")
        return None