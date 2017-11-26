import fut
import json
import time

from fut.model import dbConnector as DB
from fut.model.database import loadPlayerDatabase, executeSqlFromFile, succesTradesFromWatchlist
from fut.model.watchlist import Watchlist
from fut.model.pinAutomater import PinAutomater
from fut.model.enumeration import State
from fut.model.credentials import Credentials


credentials = Credentials()

# Verbindung zur DB
db = DB.Database(
    credentials.db['host'],
    credentials.db['user'],
    credentials.db['pass'],
    credentials.db['name']
)
pinAutomater = PinAutomater(
    credentials.mail['host'],
    credentials.mail['user'],
    credentials.mail['pass'],
    credentials.mail['port'],
)

# Verbindung zu EA
fut = fut.Core(
    credentials.ea['mail'],
    credentials.ea['pass'],
    credentials.ea['secr'],
    code=pinAutomater,
    debug=True
)

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
#items = fut.searchAuctions(ctype='player', assetId='50530358', page_size=48)
# print(items)
# items = dict()

# print(len(fut.watchlist()))

"""Objekterzeugung Watchlist"""
watchlist = Watchlist(fut)
#watchlist.loadTradeIdsFromLiveWatchlist()

"""Löschen der Watchlist anhand einer manuellen TradeIDListe"""
# trade_ids = []
# watchlist.clear(trade_ids)

"""" Tests """
#watchlist.clear()
#watchlist.fillup(items, 10)
#watchlist.loadItemsFromLiveWatchlist()

assetId         = 50530358      # Eindeutige KartenID (z.B. Rodriguez in Form)
minExpireTime   = 2            # Min expiretime in minutes
numberOfPlayers = 50            # Number of players to add to watchlist

watchlist.clear()
watchlist.sendItemsToWatchlistWithMinExpireTime(minExpireTime,numberOfPlayers, assetId)
watchlist.setExpiretime()
print(watchlist.getExpiretime())


"""" Ende Tests"""

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
