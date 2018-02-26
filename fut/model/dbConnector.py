import pymysql as MySQLdb


class Database:
    """
    Creates a database object with the database connection.
    """

    def __init__(self, host, user, password, db):
        self.connection = MySQLdb.connect(host, user, password, db, charset='utf8')
        self.cursor = self.connection.cursor()

    def insert(self, query, var=None):
        """ inserts data in database"""
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            if var != None:
                cursor.execute(query, var)
                # print("Daten eingefuegt")
            else:
                result = cursor.execute(query)
                # print("Daten eingefuegt")
            self.connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning) as err3:
            # print(err3)
            self.connection.rollback()

    def query(self, query, var=None):
        """ querys data from database """
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        if var != None:
            cursor.execute(query, var)
        else:
            cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

