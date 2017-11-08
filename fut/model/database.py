import json
import pymysql


def executeSqlFromFile(connection, filename):
    """    Oeffnet sql file, laedt enthaltene SQL-Skripte und fuehrt eines nach dem anderen aus.
    Quelle: https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python

    :param connection
    :param filename
    :rtype: String
    :return Erfolgsmessage
    :raises ValueError: Wenn SQL-Befehl fehlschlaegt
    """
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlfile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlcommands = sqlfile.split(';')

    # Execute every command from the input file

    # This will skip and report errors
    # For example, if the tables do not yet exist, this will skip over
    # the DROP TABLE commands

    for command in sqlcommands:
        connection.query(command)
        # print("Befehl ausgefuehrt: ", command)
    return


def loadPlayerDatabase(coreobject, connection):
    """    Lädt alle FUT-Spieler und schreibt sie in die Tabelle 'fut_players' in der Datenbank

    :param coreobject: fut Core Object
    :param connection: db-connection
    :rtype: String
    :return Erfolgsmessage
    """
    # players = coreobject.players
    # playerdump = json.dumps(players)
    # for key, value in players.items():
    # print(key)
    # print(value)
    #    for k, v in value.items():
    #        print(k)
    #        print(v)
    # print(playerdump)

    players = coreobject.players

    idList = []
    firstnameList = []
    lastnameList = []
    surnameList = []
    ratingList = []
    nationalityList = []

    for key, value in players.items():

        for k, v in value.items():
            if k == "firstname":
                firstnameList.append(v)
            if k == "lastname":
                lastnameList.append(v)
            if k == "id":
                idList.append(v)
            if k == "surname":
                surnameList.append(v)
            if k == "rating":
                ratingList.append(v)
            if k == "nationality":
                nationalityList.append(v)
    playerDataList = [idList, firstnameList, lastnameList, surnameList, ratingList, nationalityList]

    # q = "DROP TABLE IF EXISTS `fut_players`; CREATE TABLE IF NOT EXISTS fut_players ( ressourceId VARCHAR(15) NOT NULL, firstname VARCHAR(45) DEFAULT NULL, firstname VARCHAR(45) DEFAULT NULL, firstname VARCHAR(45) DEFAULT NULL, rating INT(3) DEFAULT NULL, nationality INT(3) DEFAULT NULL, PRIMARY KEY (ressourceId)) "
    sql = "insert into fut_players (ressourceId, firstname, lastname, surname, rating, nationality) values (%s, %s, %s, %s, %s, %s)"

    # result = connection.insert(sql, ('2', 'testname', 'testlastname', 'testsurname', 87, 12))
    result = connection.insert(sql, [idList, firstnameList, lastnameList, surnameList, ratingList, nationalityList])
    print(result)
