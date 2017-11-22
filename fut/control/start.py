import fut
import json
import os
import configparser
from fut.model import dbConnector as DB
from fut.model.database import loadPlayerDatabase, executeSqlFromFile, succesTradesFromWatchlist
from fut.model.watchlist import Watchlist
from fut.model.pinAutomater import PinAutomater
from enum import Enum


class State(Enum):
    """Creates enum for service"""
    search = 1
    chooseTrades = 2
    watchTrades = 3
    wait = 4
    saveTrades = 5
    delete = 6


def getCredentials():
    """ Lädt die Zugangsdaten für die Datenbank + Anmeldung bei EA.

    :rtype: Dictionary
    :return credentials: Zugangsdaten EA + DB
    """
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../model', 'mycredentials.conf'))

    credentials = {
        "DB_Host": config.get("configuration-DB", "host"),
        "DB_User": config.get("configuration-DB", "user"),
        "DB_Pass": config.get("configuration-DB", "pass"),
        "DB_Name": config.get("configuration-DB", "db"),
        "EA_Mail": config.get("configuration-EA", "mail"),
        "EA_Pass": config.get("configuration-EA", "pass"),
        "EA_Secr": config.get("configuration-EA", "secret"),
        "MAIL_Host": config.get("configuration-MAIL-IMAP", "host"),
        "MAIL_User": config.get("configuration-MAIL-IMAP", "user"),
        "MAIL_Pass": config.get("configuration-MAIL-IMAP", "pass"),
        "MAIL_Port": config.get("configuration-MAIL-IMAP", "port")
    }

    return credentials


credentials = getCredentials()

# Verbindung zur DB
db = DB.Database(
    credentials['DB_Host'],
    credentials['DB_User'],
    credentials['DB_Pass'],
    credentials['DB_Name']
)

pinAutomater = PinAutomater(
    credentials['MAIL_Host'],
    credentials['MAIL_User'],
    credentials['MAIL_Pass'],
    credentials['MAIL_Port'],
)

# Verbindung zu EA
fut = fut.Core(
    credentials['EA_Mail'],
    credentials['EA_Pass'],
    credentials['EA_Secr'],
    code=pinAutomater,
    debug=True
)

print(State.search is State(1))
for state in State:
    print(state)

"""create fut_players table"""
# executeSqlFromFile(db, '../model/sqlqueries/futplayers.sql')
"""create fut_watchlist table"""
# executeSqlFromFile(db, '../model/sqlqueries/futwatchlist.sql')
""" fill fut_players table """
# loadPlayerDatabase(fut, db)

"""Erfolgreiche Trades aus Watchlist in DB speichern"""
# succesTradesFromWatchlist(fut,db)


"""Test Query"""
# q = "SELECT * FROM Player"

"""Suche"""
# items = fut.searchAuctions(ctype='player', assetId='50530358', page_size=48)
# print(items)
# items = dict()

# print(len(fut.watchlist()))

"""Objekterzeugung Watchlist"""
# watchlist = Watchlist(fut)
# watchlist.clear()
# watchlist.loadTradeIdsFromLiveWatchlist()

"""Löschen der Watchlist anhand einer manuellen TradeIDListe"""
# trade_ids = []
# watchlist.clear(trade_ids)

"""Befüllen der Watchliste mit den gefundenen Items der Suche"""
# watchlist.fillup(items, 10)

# print("%s players on watchlist." % len(watchlist.loadTradeIdsFromLiveWatchlist()))
# print(fut.watchlist())

"""Löschen der Watchlist zur Laufzeit"""
# watchlist.clear()
# print("%s players on watchlist." % len(fut.watchlist()))
# print(fut.watchlist())

# backup

# for x in items:
#    print("tradeId: " + str(x["tradeId"]) + " byNowPrice: " + str(x["buyNowPrice"]) +
#          ' attributeListValue1: ' + str(x["attributeList"][0]["value"]))

# k= list(players.keys())
# lenghtk = len(k)

# for player in players:
#    for i in lenghtk:
#        print(players[k[i]])

# Ende backup

# playerInList()
# q = "SHOW DATABASES"
# q = "SHOW TABLES"

# result = db.insert(q)
# result = db.query(q)
# print(result)

# parsed = json.loads(items)
# print(json.dumps(parsed, indent=4, sort_keys=True))
# print(items)

# fut.logout()
print('start.py Done')
