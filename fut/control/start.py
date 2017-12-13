import fut
import threading

from fut.model import dbConnector as DB
from fut.model.watchlist import Watchlist
from fut.model.tradeSearcher import TradeSearcher
from fut.model.tradeChecker import TradeChecker
from fut.model.pinAutomater import PinAutomater
from fut.model.credentials import Credentials
from fut.model.database import readPlayers
from fut.model.semaphor import Semaphor
from fut.model.threadStatus import ThreadStatus
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
# fut = fut.Core(
#     credentials.ea['mail'],
#     credentials.ea['pass'],
#     credentials.ea['secr'],
#     # code=pinAutomater,
#     debug=True
# )


threadStatus = ThreadStatus()
tSearcher = None
tChecker = None
session = None


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

#assetId         = 0        # Eindeutige KartenID (z.B. Rodriguez in Form)
minExpireTimeInMinutes   = 2             # Min expiretime in minutes
maxExpireTimeInMinutes   = 5            # Max expiretime in Minutes
numberOfPlayers = 50            # Number of players to add to watchlist

# watchlist = Watchlist(fut, db, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes, numberOfPlayers)
# watchlist.startBot()
# watchlist.loadTradeIdsFromLiveWatchlist()


def createThreads(mail, passw, secr, futCore, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes, threadStatus):
    """
    Creates new fut session and two new threads for the tradeSearcher and tradeChecker
    :param mail:
    :param passw:
    :param secr:
    :param futCore:
    :param assetIds:
    :param minExpireTimeInMinutes:
    :param maxExpireTimeInMinutes:
    :param threadStatus:
    :return: session, tSearcher, tChecker
    """
    sess = futCore.Core(mail, passw, secr, debug=True)
    semaphore = Semaphor(sess)
    """ Objekterzeugung tradeSearcher und tradeChecker """
    tradeSearcher = TradeSearcher(sess, semaphore, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes,
                                  threadStatus)
    tradeChecker = TradeChecker(sess, semaphore, db, threadStatus)

    tSearch = threading.Thread(name='searcher', target=tradeSearcher.startTradeSearcher)
    tCheck = threading.Thread(name='checker', target=tradeChecker.startTradeChecker)
    return sess, tSearch, tCheck

""" Thread Erzeugung """
# tSearcher = threading.Thread(name='searcher', target=tradeSearcher.startTradeSearcher)
# tChecker = threading.Thread(name='checker', target=tradeChecker.startTradeChecker)


""" Start der Threads """
while True:
    if (tSearcher is None and tChecker is None):
        go = True
    elif (tSearcher.isAlive() is False and tChecker.isAlive() is False):
        go = True
    else:
        go = False

    if go is True:
        print('uups something happened, we will just restart the threads, lol')
        session, tSearcher, tChecker = createThreads(credentials.ea['mail'], credentials.ea['pass'],
                                                     credentials.ea['secr'], fut, assetIds, minExpireTimeInMinutes,
                                                     maxExpireTimeInMinutes, threadStatus)
        threadStatus.setSearcherStatus(True)
        threadStatus.setCheckerStatus(True)
        tSearcher.start()
        tChecker.start()

# print(fut.watchlist())

# print(threading.activeCount())
# print(tSearcher.isAlive())
# print(tChecker.isAlive())

# tradeSearcher.startTradeSearcher()
# tradeChecker.startTradeChecker()

print('start.py Done')
