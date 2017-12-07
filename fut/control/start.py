import fut
import threading

from fut.model import dbConnector as DB
from fut.model.watchlist import Watchlist
from fut.model.tradeSearcher import TradeSearcher
from fut.model.tradeChecker import TradeChecker
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


"""Objekterzeugung Watchlist"""
# assetIds = [20801, 158023, 167495, 176580, 190871, 188545, 155862, 156353, 167664, 182521, 183277, 193080, 1179, 153079, 173731, 177003, 184941, 192119, 192985, 9014, 41236, 164240, 176635, 178603, 182493, 183907, 184344, 188567, 189509, 194765, 200389, 211110, 238431]
assetIds = readPlayers(db, '../model/sqlqueries/read_playerstowatch.sql')
shuffle(assetIds)
print('test')

#assetId         = 0        # Eindeutige KartenID (z.B. Rodriguez in Form)
minExpireTimeInMinutes   = 2             # Min expiretime in minutes
maxExpireTimeInMinutes   = 5            # Max expiretime in Minutes
numberOfPlayers = 50            # Number of players to add to watchlist

# watchlist = Watchlist(fut, db, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes, numberOfPlayers)
# watchlist.startBot()
# watchlist.loadTradeIdsFromLiveWatchlist()

""" Objekterzeugung tradeSearcher und tradeChecker """
tradeSearcher = TradeSearcher(fut, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes)
tradeChecker = TradeChecker(fut, db)

""" Thread Erzeugung """
tSearcher = threading.Thread(name='searcher', target=tradeSearcher.startTradeSearcher)
tChecker = threading.Thread(name='checker', target=tradeChecker.startTradeChecker)

""" Start der Threads """
tSearcher.start()
tChecker.start()

# print(threading.activeCount())
# print(tSearcher.isAlive())
# print(tChecker.isAlive())

# tradeSearcher.startTradeSearcher()
# tradeChecker.startTradeChecker()

print('start.py Done')
