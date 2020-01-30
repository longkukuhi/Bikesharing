import sqlite3
from . import app  
from flask import g
import numpy as np
import pandas as pd
import time, datetime

import hashlib

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
#*****Registration*****
#**********************

#create user account
def createUser(email,fname,lname,password):
    try:

        # Hashing passwords
        salt = "5gz"
        password = password+salt
        hashedPassword = hashlib.sha1(password)

        user_role = 1

        current_date = ""
        cur= get_db().cursor()
        cur.execute("""INSERT INTO users (email,first_name,last_name,password,role_id,create_date)
         VALUES (?,?,?,?,?,?)""", (email,fname,lname,hashedPassword,user_role,current_date))
        get_db().commit()
        return True
    except:
        print("createUser error")
        get_db().rollback()
        return False

#update user password
#present valid old password before update or
#isreset is true, no need to present old password
def updateUserPassword(email,oldpassword,newpassword,isreset=False):
    return True

#**********************
#*****Login       *****
#**********************
#Login, return user role and session no. after valid password check
def doLogin(email,password):
    try:
        # Creating hash
        salt = "5gz"
        password = password+salt
        hashedPass = hashlib.sha1(password)

        cur= get_db().cursor()
        cur.execute("SELECT role_id, user_id, isActive, password FROM users WHERE email = ?", [email])
        row= cur.fetchone()
        role_id= row[0]
        user_id= row[1]
        isActive= row[2]
        secret= row[3]
        if hashPass == secret and isActive == 1: #login success
            session_ran = np.random.randint(0,10,7)
            session_no=""
            for unit in session_ran:
                session_no= session_no + str(unit)
            return (True, role_id, user_id, session_no)
        else:
            return (False,-1,'','')
    except:
        print("doLogin error")
        return (False,-1,'','') 

#+++++++++++Customer+++++++++++

# **********************
# * GetPersonalInfo *
# **********************
# Update the personal info-checked-need exception modify


def getPersonalInfo(user_id):
    try:
        cur = get_db().cursor()
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
        return (email,phone_number,first_name,last_name,address,post_code,city,country)
    except:
        print("Fail to read personal info")
        raise


# **********************
# * UpdatePersonalInfo *
# **********************
# Update the personal info-checked-need exception modify


def updatePersonalInfo(user_id,email,phone_number,first_name,last_name,address,post_code,city,country):
    try:
        cur = get_db().cursor()
        cur.execute(
        "UPDATE users SET email = ?, phone_number = ?, first_name = ?, last_name = ?, address = ?, post_code = ?, city = ?, country = ?  where user_id = ?", (
        email, phone_number, first_name, last_name, address, post_code, city, country, user_id))
        get_db().commit()
        return True
    except:
        print("Fail to update personal info")
        return False

# Close user account

def deactivateUser(user_id,email):
    try:
        cur = get_db().cursor()
        cur.execute(
        "UPDATE users SET isActive = 0 WHERE user_id = ? AND email = ?", (
        user_id, email))
        get_db().commit()
        if  cur.rowcount == 1:
            return 1
        else:
            return 0
    except:
        print("Fail to deactivateUser")
        raise


# Update payment card info

def updateCardInfo(user_id,card_num,card_name,exp_mm,exp_yy,cvv):
    try:
        cur = get_db().cursor()
        cur.execute(
        "SELECT COUNT(*) FROM accounts where user_id = ?", [user_id])
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


# Get default card info to page


def getCardInfo(user_id):
    try:
        cur = get_db().cursor()
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
        return card_num, card_name, exp_mm, exp_yy, cvv
    except:
        print("Fail to get Card Info")
        raise


#**********************
#*****Report Defect****
#**********************

#Create Defect incident
#Status set as DEFECT
def createDefectReport(user_id,bike_id,category,details):
    try:
        cur = get_db().cursor()
        timestamp = time.localtime(time.time())
        #timerecord = time.strftime('%Y%m%d%H%M%S', timestamp)
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

#**********************
#*****Rent/Return *****
#**********************

#Create order releted to rent action, return order_id,status set INUSE
def createOrder(user_id,bike_id):
    try:
        cur = get_db().cursor()
        timestamp = time.localtime(time.time())
        start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)

        cur.execute("INSERT INTO orders (user_id, bike_id, start_datetime) VALUES (?, ?, ?)",(user_id, bike_id,start_datetime))
        get_db().commit()
        cur.execute("SELECT last_insert_rowid()")
        result = cur.fetchone()
        return (True, result[0])
    except:
        print("Fail to create order!")
        return (False, -1)

#Update order releted to return action, to complete a order transaction, status set AVAILABLE
def settleOrder(order_id):
    try:
        cur = get_db().cursor()
        cur.execute("SELECT start_datetime FROM orders WHERE order_id = ?", [order_id])
        str_start_datetime = str(cur.fetchone()[0])
        str_end_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        start_datetime= datetime.datetime.strptime(str_start_datetime,'%Y-%m-%d %H:%M:%S')
        end_datetime= datetime.datetime.strptime(str_end_datetime,'%Y-%m-%d %H:%M:%S')
        delta= end_datetime - start_datetime

        amount = round(delta.seconds/60 * RATE,2)

        cur.execute("UPDATE orders SET end_datetime = ?,amount = ? WHERE order_id = ?", (str_end_datetime,amount,order_id))
        get_db().commit()
        return True, amount
    except:
        print("Fail to settle Order")
        return False, 0
    return True

#Update bike location and status
def updateBikeState(bike_id, status, lat=-1, long=-1, park_loc_id=1):
    try:
        cur = get_db().cursor()
        if status == 'A':
            cur.execute("UPDATE bikes SET parked_bike_station=?, status=? WHERE bike_id =?", (park_loc_id, status, bike_id))
        elif status == 'D':
            cur.execute("UPDATE bikes SET status=? WHERE bike_id =?", (status, bike_id))       
        elif status == 'U':
            cur.execute("UPDATE bikes SET status=? WHERE bike_id =?", (status, bike_id))
        else:
            cur.execute("UPDATE bikes SET loc_lat=?, loc_long=? WHERE bike_id =?", (lat, long, status, bike_id))
        get_db().commit()
        return True
    except:
        print("Fail to update bike")
        return False

#**********************
#*****Charge/Pay  *****
#**********************

#Create one if a not existing in user account
#Deduce amount from user account, isTopup is false
#Top up acccount balance, for isTopup is true
def updateAccountBalance(user_id,amount,cardinfo,isTopup=True):
    return True


#+++++++++++Operator+++++++++++

#**********************
#*****Track bikes  ****
#**********************

#Return list of bikes with loc. info and status
def trackbikes():
    try:
        bikeid= []
        locs=[]
        cur= get_db().cursor()
        cur.execute("SELECT bike_id, loc_lat, loc_long FROM bikes")
        for row in cur.fetchall():
            bikeid.append(row[0])
            locs.append({'lat': row[1] , 'lng': row[2] })

        return (bikeid,locs)
    except:
        print("trackbikes error")
        return None

#**********************
#*****Repair Defect****
#**********************

#Show dash board
#Status as DEFECT
def getDashBoardFig():
    try:
        results= {}
        cur= get_db().cursor()
        cur.execute("SELECT status, count(*) FROM bikes GROUP BY status")
        for row in cur.fetchall():
            results[row[0]]= row[1]

        cur.execute("SELECT count(*) from defect_report WHERE status <> 'DF'")
        count= cur.fetchone()
        results['T']=count[0]

        return results
    except:
        print("showDashBoardFig error")
        return None 

#Show outstanding defects
#Status as DEFECT
def showDefectReport():
    try:
        cur= get_db().cursor()
        cur.execute("""SELECT D.report_id, U.email, D.bike_id, D.category, 
        D.details, D.report_datetime, D.status FROM defect_report D, 
        users U on D.user_id = U.user_id where status <> 'DF'""")
        rows=  cur.fetchall()

        return (rows)
    except:
        print("showDefectReport error")
        return None

#Change defect status
#Status as RD-REP_DEFECT/RI-REP_INVESTIGATE/DF-FIXED
def updateDefectStatus(id, new_status):
    try:
        cur= get_db().cursor()
        cur.execute("UPDATE defect_report SET status=? where report_id = ?", (new_status, id))
        get_db().commit()
        return True
    except:
        print("updateDefectStatus")
        get_db().rollback()
        return False

#**********************
#*****Move Bikes   ****
#**********************


#Show bikes that require move action, bikes station lack of bike or overcrowded
def showBikeStations():
    try:

        sql1="""SELECT count(*) as 'num_bikes', parked_bike_station FROM bikes WHERE status <> 'U' 
        GROUP BY parked_bike_station"""

        sql2="SElECT station_id, post_code, loc_lat, loc_long, bike_rack_number FROM bike_stations"
        bikescountfrm= pd.read_sql_query(sql1,get_db())
        stationfrm= pd.read_sql_query(sql2,get_db())

        resultset= pd.merge(stationfrm,bikescountfrm,how='outer',left_on='station_id',right_on='parked_bike_station')
        resultset['occ_rate']=round(resultset['num_bikes']/resultset['bike_rack_number']*100,2)
        return (resultset)
    except:
        print("showBikeStations error")
        return None

#manager
def createDate(startdate,enddate):
   try:
        cur = get_db().cursor()
        cur.execute("""INSERT INTO datepick (startdate,enddate)
         VALUES (?,?)""", (startdate,enddate))
        get_db().commit()
        return True
    except:
        print("Fail to update personal info")
        return False