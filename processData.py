from malipulate_database import *
from generateData_method import *
from visual_method import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


originalData = pd.read_csv('train.csv')

#slice
# df = originalData.iloc[:1000]
# order = genConcreteData(df)
# order.to_csv('dataset_1000.csv')
# order.to_excel('dateset_1000.xlsx')

database = 'bikehistoryall.db'
db = connet_datebase(database)
# query = '''CREATE TABLE IF NOT EXISTS order (date text, start_time_hour integer,
#             strat_time_minutes integer, end_time_hour integer,
#             end_time_minutes integer, total_fee integer, bike_id integer,
#              user_id integer, workingday boolean, season integer, weather integer,
#              temp real, atemp real,humidity real, windspeed ,real);'''
# db.execute(query)
# db.commit()
originalData.info()
originalData.to_sql('alldata',db,if_exists='replace')
# db.commit()


# sql_query = 'SELECT * FROM history'
# df = pd.read_sql(sql_query, con=db)
# df.to_csv("test.txt")
# df.info()
# #df = pd.read_sql_query("SELECT * FROM order", db)
# print(df)
#
# a = np.load('test.txt')
# print(a)
# query = """INSERT INTO order2 VALUES('adcasdcd','scdd', 12, 25.0)"""
# db.execute(query)
# db.commit()
# a = input()
# b = input()
# c = input()
# d = input()
# query = """INSERT INTO BIKEORDER VALUES(?,?,?,?)"""
# db.execute(query,(a,b,c,d))
# db.commit()



# query = "select bikeorder.a, bikeorder.b,order2.a,order2.b " \
#         "from bikeorder,order2 where bikeorder.c = order2.c and order2.d >23"
# cursor = db.execute(query)
# showQuery(cursor)
#db.commit()

# whichnumber = input()
# query = 'select * from order2 where c=?'
# cursor = db.execute(query,[whichnumber])
# showQuery(cursor)
# db.commit()

# query = 'update order2 set c=15 where d=25'
# db.execute(query)
# db.commit()


# query = 'select * from order'
# cursor = db.execute(query)
# showQuery(cursor)
# db.commit()

db.close()
