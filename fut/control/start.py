import fut
import threading

from fut.model import dbConnector as DB
from fut.model.checkPacks import CheckPacks
from fut.model.checkSBC import CheckSBC
from fut.model.tradeSearcher import TradeSearcher
from fut.model.tradeChecker import TradeChecker
from fut.model.pinAutomater import PinAutomater
from fut.model.credentials import Credentials
from fut.model.database import readPlayers
from fut.model.semaphor import Semaphor
from fut.model.threadStatus import ThreadStatus
from random import shuffle
from slackclient import SlackClient
import time
import datetime


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

slack_client = SlackClient(credentials.slack['slack_token'])
botName = 'Bot_3(ZD-Auner): '
#Wenn diese Variable auf True ist werden Packs und SBCs bei dem Bot geladen.
isPackSearcher = False

threadStatus = ThreadStatus()
tSearcher = None
tChecker = None
session = None
tSlacker = None
tPacks = None
tSBCs = None


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


def createThreads(mail, passw, secr, futCore, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes, threadStatus, slack_client, nameBot):
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
    sess = futCore.Core(slack_client, nameBot, mail, passw, secr, debug=True)

    semaphore = Semaphor(sess, slack_client, nameBot)
    """ Objekterzeugung tradeSearcher und tradeChecker """
    tradeSearcher = TradeSearcher(sess, semaphore, assetIds, minExpireTimeInMinutes, maxExpireTimeInMinutes,
                                  threadStatus, slack_client, nameBot)
    tradeChecker = TradeChecker(sess, semaphore, db, threadStatus, slack_client, nameBot)


    tSearch = threading.Thread(name='searcher', target=tradeSearcher.startTradeSearcher)
    tCheck = threading.Thread(name='checker', target=tradeChecker.startTradeChecker)

    return sess, tSearch, tCheck

""" Thread Erzeugung """
# tSearcher = threading.Thread(name='searcher', target=tradeSearcher.startTradeSearcher)
# tChecker = threading.Thread(name='checker', target=tradeChecker.startTradeChecker)


""" Start der Threads """
while True:
    if isPackSearcher is False:
        if tSearcher is None and tChecker is None:
            go = True
        elif tSearcher.isAlive() is False and tChecker.isAlive() is False:
            go = True
        else:
            go = False

        if go is True:
            print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] Start: uups something happened, we will just restart the threads, lol')
            session, tSearcher, tChecker = createThreads(credentials.ea['mail'], credentials.ea['pass'],
                                                         credentials.ea['secr'], fut, assetIds, minExpireTimeInMinutes,
                                                         maxExpireTimeInMinutes, threadStatus, slack_client, botName)
            threadStatus.setSearcherStatus(True)
            threadStatus.setCheckerStatus(True)
            tSearcher.start()
            tChecker.start()

    else:
        if tSearcher is None and tChecker is None and tSBCs is None and tPacks is None:
            go = True
        elif tSearcher.isAlive() is False and tChecker.isAlive() is False and tSBCs.is_alive() is False and tPacks.is_alive() is False:
            go = True
        else:
            go = False

        if go is True:
            print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                  '] Start: uups something happened, we will just restart the threads, lol')
            session, tSearcher, tChecker = createThreads(credentials.ea['mail'], credentials.ea['pass'],
                                                         credentials.ea['secr'], fut, assetIds, minExpireTimeInMinutes,
                                                         maxExpireTimeInMinutes, threadStatus, slack_client, botName)
            threadStatus.setSearcherStatus(True)
            threadStatus.setCheckerStatus(True)
            tSearcher.start()
            tChecker.start()

            checkSBC = CheckSBC(session, db, isPackSearcher, threadStatus)
            tSBCs = threading.Thread(name='SBCs', target=checkSBC.sbcsInFut)
            checkPacks = CheckPacks(session, db, isPackSearcher, threadStatus)
            tPacks = threading.Thread(name='packer', target=checkPacks.packsInFUT)

            tPacks.start()
            tSBCs.start()






# print(fut.watchlist())

# print(threading.activeCount())
# print(tSearcher.isAlive())
# print(tChecker.isAlive())

# tradeSearcher.startTradeSearcher()
# tradeChecker.startTradeChecker()

print('start.py Done')


