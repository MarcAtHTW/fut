import pymysql as MySQLdb
import sys
from pymysql import cursors

class Database:

    def __init__(self, host, user, password, db):
        self.connection = MySQLdb.connect(host, user, password, db)
        self.cursor = self.connection.cursor()

    def insert(self, query, var=None):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            if var != None:
                cursor.execute(query, var)
                print("Daten eingefuegt")
            else:
                result = cursor.execute(query)
                print("Daten eingefuegt")
            self.connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning) as err3:
            print(err3)
            self.connection.rollback()

    def query(self, query, var=None):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        if var != None:
            cursor.execute(query, var)
        else:
            cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

