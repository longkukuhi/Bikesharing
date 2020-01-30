import sqlite3

with sqlite3.connect("bikerenting.db") as db:
	cursor=db.cursor()

#users table contains user registration and authentication information
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
	"user_id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"email"	INTEGER NOT NULL UNIQUE,
	"phone_number"	INTEGER,
	"first_name"	TEXT,
    "last_name"	TEXT,
    "address"	TEXT,
    "post_code"	TEXT,
    "city"	TEXT,
    "country"	TEXT,
	"password"	TEXT NOT NULL,
	"role_id"	INTEGER NOT NULL,
	"create_date"	TEXT NOT NULL,
    "close_date"	TEXT,
    "isActive"	INTEGER DEFAULT 1,
	FOREIGN KEY("role_id") REFERENCES "user_roles"("role_id")
);""")

#user_roles table contains user role in system 
#1-customer
#2-operator
#3-manager

cursor.execute("""CREATE TABLE IF NOT EXISTS user_roles (
	"role_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"description"	TEXT
);""")

#orders table contains RENT/RETURN transaction details
cursor.execute("""CREATE TABLE IF NOT EXISTS "orders" (
	"order_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"bike_id"	INTEGER NOT NULL,
	"start_datetime"	TEXT NOT NULL,
	"end_datetime"	TEXT,
	"amount"	REAL DEFAULT 0,
	FOREIGN KEY("bike_id") REFERENCES "bikes"("bike_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);""")

#bikes table contains bike info. and it's corresponding location status can be DEFECT/AVAILABLE/PENDING_ACTION/INUSE

cursor.execute("""CREATE TABLE IF NOT EXISTS "bikes" (
	"bike_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"status"	TEXT NOT NULL,
	"parked_bike_station"	INTEGER,
	"loc_lat"	REAL,
	"loc_long"	REAL,
	FOREIGN KEY("parked_bike_station") REFERENCES "bike_stations"("station_id")
);""")

#bike_stations table contains bike station info. including it's location, bikes are parked there before RETURN action
cursor.execute("""CREATE TABLE IF NOT EXISTS "bike_stations" (
	"station_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name" TEXT,
	"post_code"	TEXT,
	"loc_lat"	REAL NOT NULL,
	"loc_long"	REAL NOT NULL,
	"bike_rack_number"	INTEGER NOT NULL
);""")

#defect_report table contains defects reported by customers status can be REP_DEFECT/REP_INVESTIGATE/FIXED 
cursor.execute("""CREATE TABLE IF NOT EXISTS "defect_report" (
	"report_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"bike_id"	INTEGER NOT NULL,
	"category"	INTEGER NOT NULL,
	"details"	BLOB,
	"report_datetime"	TEXT NOT NULL,
	"status"	TEXT NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
	FOREIGN KEY("bike_id") REFERENCES "bikes"("bike_id")
);""")


#accounts table contains balance of users
cursor.execute("""CREATE TABLE IF NOT EXISTS "accounts" (
	"user_id"	INTEGER NOT NULL PRIMARY KEY UNIQUE,
    "card_number" TEXT,
    "card_holder" TEXT,
	"exp_mm" TEXT,
    "exp_yy" TEXT,
    "cvv_digits" TEXT,
	"total_amount"	REAL NOT NULL DEFAULT 0,
	"last_topup_datetime"	TEXT,
	"last_topup_amount"	REAL,
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);""")

# table for manager page
cursor.execute("""CREATE TABLE IF NOT EXISTS "alldata" (
	"index"	INTEGER,
	"datetime"	TEXT,
	"season"	INTEGER,
	"holiday"	INTEGER,
    "workingday"	INTEGER,
    "weather"	INTEGER,
    "temp"	REAL,
    "atemp"	REAl,
    "humidity"	INTEGER,
	"windspeed"	REAL,
	"casual"	INTEGER,
	"registered" INTEGER,
    "count"	INTEGER);""")




#user role table initializaton
cursor.execute("""INSERT INTO user_roles (role_id, description) VALUES (1, 'Customer'), 
				(2, 'Operator'), 
				(3, 'Manager')""")

#bike stations testing data loading
cursor.execute("""INSERT INTO bike_stations (station_id,name,post_code,loc_lat,loc_long,bike_rack_number) VALUES (1,'Cowcaddens','G40BA',55.86729,-4.25006,10),
				(2,'Blythswood Hill','G25RJ',55.86248,-4.26362,8),
				(3, 'Merchant City', 'G11XQ',55.86125,-4.24471,8),
				(4,'Gorbals','G59TA',55.85254,-4.25184,20),
				(5,'Hillhead','G128AF',55.8756,-4.291,3)""")

#bikes testing data loading
cursor.execute("""INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1001,'A',1,55.86729,-4.25006),
				(1002,'A',1,55.86729,-4.25006),
				(1003,'A',1,55.86729,-4.25006),
				(1004,'A',1,55.86729,-4.25006),
				(1005,'A',2,55.86248,-4.26362),
				(1006,'A',2,55.86248,-4.26362),
				(1007,'A',3,55.86125,-4.24471),
				(1008,'A',3,55.86125,-4.24471),
				(1009,'A',4,55.85254,-4.25184),
				(1010,'A',4,55.85254,-4.25184),
				(1011,'A',4,55.85254,-4.25184),
				(1012,'D',4,55.85254,-4.25184),
				(1013,'U',4,55.86222,-4.25555),
				(1014,'A',5,55.8756,-4.291),
				(1015,'A',5,55.8756,-4.291),
				(1016,'A',5,55.8756,-4.291)""")

#defect ticket testing data loading
cursor.execute("""INSERT INTO defect_report (user_id,bike_id,category,details,report_datetime,status) VALUES (1,1012,'Others','no brake','2019-10-14 13:30','RD'),
				(1,1013,'Others','broken chair','2019-10-15 12:30','RI'),
				(1,1014,'Others','broken light','2019-10-18 11:30','DF'),
				(1,1015,'Others','not function','2019-10-12 12:30','RD'),
				(1,1007,'Others','wonderful','2019-10-11 16:30','RD')""")


#user account for user, admin and operator for testing purpose
cursor.execute("""INSERT INTO users (email, first_name, role_id, password, create_date) VALUES ('user@gmail.com','user a',1,'3a902cab89e1edf7665c5e12394c86d0dda1e6d4','2019-10-12 12:30')""")
cursor.execute("""INSERT INTO users (email, first_name, role_id, password, create_date) VALUES ('admin@gmail.com','admin a',3,'3a902cab89e1edf7665c5e12394c86d0dda1e6d4','2019-10-12 12:30')""")
cursor.execute("""INSERT INTO users (email, first_name, role_id, password, create_date) VALUES ('oper@gmail.com','oper a',2,'3a902cab89e1edf7665c5e12394c86d0dda1e6d4','2019-10-12 12:30')""")
db.commit()
cursor.execute("select * from user_roles")
for x in cursor.fetchall():
    print(x)

cursor.execute("select * from orders")
for x in cursor.fetchall():
    print(x)
    
cursor.execute("select * from bike_stations")
for x in cursor.fetchall():
    print(x)
    
cursor.execute("select * from bikes")
for y in cursor.fetchall():
    print(y)
    
cursor.execute("select * from defect_report")
for y in cursor.fetchall():
    print(y)