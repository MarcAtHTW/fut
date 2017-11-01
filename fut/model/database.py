import json


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
    for command in sqlcommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            with connection.cursor() as cursor:
                cursor.execute(command)
                # connection.commit()
                print("Befehl ausgefuehrt: ", command)
        except ValueError as msg:
            print("Command skipped: ", msg)
    return


def createAndLoadPlayerDatabase(coreobject, connection, filename):
    """    Lädt alle FUT-Spieler und schreibt sie in die Tabelle 'fut_players' in der Datenbank, wenn die Tabelle noch nicht existiert wird sie erzeugt

    :param coreobject: fut Core Objekt
    :param connection: db-conneciton
    :param filename: sql filename
    :rtype: String
    :return Erfolgsmessage
    """
    players = coreobject.players
    playerdump = json.dumps(players)
    for key, value in players.items():
        # print(key)
        # print(value)
        for k, v in value.items():
            print(k)
            print(v)
    # print(playerdump)
    executeSqlFromFile(connection, filename)
    # q = "DROP TABLE IF EXISTS `fut_players`; CREATE TABLE IF NOT EXISTS fut_players ( ressourceId VARCHAR(15) NOT NULL, firstname VARCHAR(45) DEFAULT NULL, firstname VARCHAR(45) DEFAULT NULL, firstname VARCHAR(45) DEFAULT NULL, rating INT(3) DEFAULT NULL, nationality INT(3) DEFAULT NULL, PRIMARY KEY (ressourceId)) "
    try:
        connection.executemany(
            "insert into fut_players (ressourceId, firstname, lastname, surname, rating, nationality) values (%s, %s, %s, %s, %s, %s)",
            playerdump)
        # connection.commit()
    except ValueError as msg:
        print("Command skipped: ", msg)

    return print("database fut_players created data loaded")
