import sqlite3

def connet_datebase(dbName):
    db = sqlite3.connect(dbName)
    return db

def showQuery(cursor):
    rows = cursor.fetchall()
    for row in rows:
        print(row)

