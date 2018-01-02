from fut.model.enumeration import State
import time
import datetime
from random import shuffle

class TradeSearcher:
    def __init__(self, fut_session, semaphore, assetIds, minExpireTime, maxExpireTimeinMinutes, threadStatus, slack_client, botName):
        self.assetId = 0
        self.assetIds = assetIds
        self.minExpireTimeInMinutes = minExpireTime
        self.maxExpireTimeinMinutes = maxExpireTimeinMinutes
        self.session = fut_session
        self.semaphore = semaphore
        # self.tradepile = fut_session.tradepile()
        self.length = len(fut_session.watchlist())
        self.watchlistSize = fut_session.watchlist_size
        self.expire = {}
        self.tradeIDs = []
        self.currentState = State.pending
        self.watchlist = fut_session.watchlist()
        self.numberOfPlayers = 50
        self.error = False
        self.threadStatus = threadStatus
        self.slack_client = slack_client
        self.botName = botName

    def startTradeSearcher(self):

        print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] ### TradeSearcher started ###')

        while self.error is False:
            shuffle(self.assetIds)
            if self.threadStatus.getCheckerStatus() is False:
                self.error = True
            else:
                for assetId in self.assetIds:
                    if self.error == True:
                        break
                    print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] TradeSearcher: Current ressource ID: {}'.format(assetId))
                    self.assetId = assetId
                    """ Search Trades for current assetId"""
                    self.searchAsset(self.minExpireTimeInMinutes, self.maxExpireTimeinMinutes, assetId)
        self.threadStatus.setSearcherStatus(False)


    def searchAsset(self, minExpireTimeInMinutes, maxExpireTimeinMinutes, assetId):
        """
        This method searches once for each assetId, as soon as a valid trade between min- and maxExpireTime is found, it's added to the watchlist.
        If there are no new trade trades for three pages in the search, the loop breaks.
        :param minExpireTimeInMinutes:
        :param maxExpireTimeinMinutes:
        :param assetId:
        :return:
        """
        self.currentState = State.search

        minExpireTimeInSeconds = minExpireTimeInMinutes * 60
        maxExpireTimeInSeconds = maxExpireTimeinMinutes * 60
        currentPage = 1
        tradeCounter = 0
        noNewTradeCounter = 0
        items_resultset = []

        self.currentState = State.search
        try:
            items_resultset = self.session.searchAuctions(ctype='player', assetId=assetId, start=currentPage,
                                                          page_size=25)
        except Exception as error:
            print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] {Debug} An error in the tradeSearcher has occurred: search failed: ', error)
            self.error = True

        self.currentState = State.chooseTrades
        if len(items_resultset) > 0:
            for item in items_resultset:
                if self.error == True:
                    break
                elif item['expires'] > minExpireTimeInSeconds and item[
                    'expires'] < maxExpireTimeInSeconds and tradeCounter <= 5:
                    self.saveToWatchlist(item['tradeId'])
                    tradeCounter += 1
                else:
                    noNewTradeCounter += 1
                if tradeCounter >= 5 or noNewTradeCounter >= 10:
                    break


    def getIdsFromPage(self, page):
        """ Gets all ID's from Current q Resultset.
        :param page: Pages (Resultset) of transfermarketsearch.
        :type page: dict
        :return:
        """
        listIds = []
        for item in page:
            listIds.append(item['id'])
        return listIds

    def saveToWatchlist(self, tradeId):
        """ Sends current tradeId to watchlist
        :param tradeId: tradeId of current trade
        """
        try:
            self.length = len(self.session.watchlist())
        except Exception as error:
            print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] {Debug} An error in the tradeSearcher has occurred: len watchlist failed: ', error)
            self.error = True
        self.currentState = State.watchTrades
        self.loadTradeIdsFromLiveWatchlist()

        while tradeId not in self.tradeIDs and self.error is False:
            if self.threadStatus.getCheckerStatus() is False:
                self.error = True
            else:
                if self.length < self.watchlistSize:
                    try:
                        self.error = self.semaphore.search(int(tradeId))
                        print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] TradeSearcher: Player with TradeID {} added to Watchlist.'.format(tradeId))
                    except Exception as error:
                        print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] {Debug} An error in the tradeSearcher while-loop has occurred: ', error)
                        self.error = True
                    break
                else:
                    time.sleep(2)
                    try:
                        self.length = len(self.session.watchlist())
                    except Exception as error:
                        print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] {Debug} An error in the tradeSearcher has occurred: No free slot, update length watchlist: ',
                              error)
                        self.error = True

    def loadTradeIdsFromLiveWatchlist(self):
        """ Gets the current live Trade-IDs from watchlist and loads it into local property tradeIDs
        :rtype: list
        :return:  live Trade-IDs from watchlist.
        """
        tradeIds = []
        resultset = []
        try:
            resultset = self.session.watchlist()
        except Exception as error:
            print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] {Debug} An error in the tradeSearcher has occurred: get watchlist: ', error)
            self.error = True
        for item in resultset:
            tradeIds.append(item['tradeId'])
        self.tradeIDs = tradeIds
        return self.tradeIDs