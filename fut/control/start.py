import fut

from fut.model import dbConnector as DB
from fut.model.watchlist import Watchlist
from fut.model.pinAutomater import PinAutomater
from fut.model.credentials import Credentials
from fut.model.database import readPlayers
from random import shuffle



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
    #code=pinAutomater,
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
#items = fut.searchAuctions(ctype='player', page_size=48)
# print(items)
# items = dict()

# print(len(fut.watchlist()))

"""Objekterzeugung Watchlist"""
# assetIds = [20801, 158023, 167495, 176580, 190871, 188545, 155862, 156353, 167664, 182521, 183277, 193080, 1179, 153079, 173731, 177003, 184941, 192119, 192985, 9014, 41236, 164240, 176635, 178603, 182493, 183907, 184344, 188567, 189509, 194765, 200389, 211110, 238431]
assetIds = readPlayers(db, '../model/sqlqueries/read_playerstowatch.sql')
shuffle(assetIds)

#assetId         = 0        # Eindeutige KartenID (z.B. Rodriguez in Form)
minExpireTimeInMinutes   = 2             # Min expiretime in minutes
maxExpireTimeInMinutes   = 5            # Max expiretime in Minutes
numberOfPlayers = 50            # Number of players to add to watchlist

watchlist = Watchlist(fut, db, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes, numberOfPlayers)
watchlist.startBot()
#watchlist.loadTradeIdsFromLiveWatchlist()

"""Löschen der Watchlist anhand einer manuellen TradeIDListe"""
# trade_ids = []
# watchlist.clear(trade_ids)

"""" Tests """
#watchlist.clear()
#watchlist.fillup(items, 10)
#watchlist.loadItemsFromLiveWatchlist()

### old loop - start ###



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
