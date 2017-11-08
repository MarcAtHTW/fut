import fut
import json
import os
import configparser
from fut.model import dbConnector as DB
from fut.model.database import createAndLoadPlayerDatabase

def getCredentials():
    """    Lädt die Zugangsdaten für die Datenbank + Anmeldung bei EA.

    :rtype: Dictionary
    :return credentials: Zugangsdaten EA + DB
    """
    config  = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../model', 'mycredentials.conf'))

    credentials = {
        "DB_Host" : config.get("configuration-DB", "host"),
        "DB_User" : config.get("configuration-DB", "user"),
        "DB_Pass" : config.get("configuration-DB", "pass"),
        "DB_Name" : config.get("configuration-DB", "db"),
        "EA_Mail" : config.get("configuration-EA", "mail"),
        "EA_Pass" : config.get("configuration-EA", "pass"),
        "EA_Secr" : config.get("configuration-EA", "secret")
    }

    return credentials

credentials = getCredentials()

#Verbindung zur DB
db = DB.Database(
    credentials['DB_Host'],
    credentials['DB_User'],
    credentials['DB_Pass'],
    credentials['DB_Name']
)

#Verbindung zu EA
fut = fut.Core(
    credentials['EA_Mail'],
    credentials['EA_Pass'],
    credentials['EA_Secr'],
    debug=True
)

# create and fill fut_players table
# createAndLoadPlayerDatabase(fut, db, '../model/sqlqueries/futplayers.sql')





#Test Query
# q = "SELECT * FROM Player"

#Suche
items = fut.searchAuctions(ctype='player', level='gold', assetId = '50530358')

#JSON Dump

# player ist eine freie Variable
# items in die Liste in der die Suchergebnisse gespeichert werden

#sucheSpeichern()

def sucheSpeichern():

    tradeIdList = []

    for suche in items:
        tradeIdList.append(x["tradeId"])



#Testschleifen
#for player in items:
#    print (player['tradeId'])
#    print(player)


#for x in items:
#    print("tradeId: " + str(x["tradeId"]) + " byNowPrice: " + str(x["buyNowPrice"]) +
#          ' attributeListValue1: ' + str(x["attributeList"][0]["value"]))




#k= list(players.keys())
#lenghtk = len(k)

#for player in players:
#    for i in lenghtk:
#        print(players[k[i]])

# Definition von Listen und Füllung dieser mit Player Inhalt

def playerInList():
    players = fut.players

    idList = []
    firstnameList = []
    lastnameList = []
    surnameList = []
    ratingList = []
    nationalityList = []

    for key, value in players.items():
        #print(key)
        #print(value)
        for k,v in value.items():
            if k == "firstname":
                #print(k)
                firstnameList.append(v)
            if k == "lastname":
                #print(k)
                lastnameList.append(v)
            if k == "id":
                #print(k)
                idList.append(v)
            if k == "surname":
                #print(k)
                surnameList.append(v)
            if k == "rating":
                #print(k)
                ratingList.append(v)
            if k == "nationality":
                #print(k)
                nationalityList.append(v)



#Ende Testschleifen


#dump = json.dumps(items)
#with open('data.txt', 'w') as outfile:
#    json.dump(dump, outfile)


#q = "SHOW DATABASES"
#q = "SHOW TABLES"

#result = db.insert(q)
#result = db.query(q)
#print(result)

#parsed = json.loads(items)
#print(json.dumps(parsed, indent=4, sort_keys=True))
#print(items)

#players = fut.players
#nations = fut.nations()

#leagues = fut.leagues()
#teams = fut.teams()
#stadiums = fut.stadiums()
#players = fut.players()
#playestyles = fut.playstyles()

#fut.logout()
print('Done')