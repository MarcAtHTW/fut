from fut.model.enumeration import State
import time
from random import shuffle

class TradeSearcher:
    def __init__(self, fut_session, semaphore, assetIds, minExpireTime, maxExpireTimeinMinutes, threadStatus):
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

    def startTradeSearcher(self):
        print('### TradeSearcher started ###')
        """ Clear Watchlist at startup. """
        # self.clear()
        while self.error is False:
            if self.threadStatus.getCheckerStatus() is False:
                self.error = True
                shuffle(self.assetIds)
            else:
                for assetId in self.assetIds:
                    print('(Debug): Current ressource ID: {}'.format(assetId))
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
        print(self.currentState)

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
            print('{Debug} An error in the tradeSearcher has occurred: search failed: ', error)
            self.error = True

        print('{} From Page {}'.format(self.currentState, currentPage))
        self.currentState = State.chooseTrades
        if len(items_resultset) > 0:
            for item in items_resultset:
                if item['expires'] > minExpireTimeInSeconds and item[
                    'expires'] < maxExpireTimeInSeconds and tradeCounter <= 5:
                    self.saveToWatchlist(item['tradeId'])
                    tradeCounter += 1
                else:
                    noNewTradeCounter += 1
                if tradeCounter >= 5 or noNewTradeCounter >= 10:
                    break
            print('Break due to tradeCounter: ', tradeCounter)
            print('Break due to noNewTradeCounter: ', noNewTradeCounter)
        else:
            print('#### No trades in search result')


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
            print('{Debug} An error in the tradeSearcher has occurred: len watchlist failed: ', error)
            self.error = True
        self.currentState = State.watchTrades

        print('trades on watchlist: ', self.length)

        self.loadTradeIdsFromLiveWatchlist()
        # TODO Was ist wenn TradeId immer auf der Watchlist ist(TradeIds) und die While übersprungen wird? (Bug zur Laufzeit erkannt TradeCounter = 5 obwohl nichts auf die Watchlist gesetzt wurde)
        while tradeId not in self.tradeIDs and self.error is False:
            if self.threadStatus.getCheckerStatus() is False:
                self.error = True
            else:
                if self.length < self.watchlistSize:
                    try:
                        self.error = self.semaphore.search(int(tradeId))
                        #self.session.sendToWatchlist()
                        print("Player with TradeID {} added to Watchlist.".format(tradeId))
                    except Exception as error:
                        print('{Debug} An error in the tradeSearcher while-loop has occurred: ', error)
                        self.error = True
                    break
                else:
                    print('No free slot on Watchlist. Waiting for 2 sec.')
                    time.sleep(2)
                    try:
                        self.length = len(self.session.watchlist())
                    except Exception as error:
                        print('{Debug} An error in the tradeSearcher has occurred: No free slot, update length watchlist: ',
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
            print('{Debug} An error in the tradeSearcher has occurred: get watchlist: ', error)
            self.error = True
        for item in resultset:
            tradeIds.append(item['tradeId'])
        self.tradeIDs = tradeIds
        return self.tradeIDs

    def clear(self, listTradeIds=None):
        self.currentState = State.delete
        print(self.currentState)
        """ Clears the current watchlist.
        :type listTradeIds: list
        :param listTradeIds: List of tradeIDs. Can be used to manually delete items from watchlist.
        """
        if listTradeIds == None:
            self.loadTradeIdsFromLiveWatchlist()
            lenItemsOnWatchlist = len(self.tradeIDs)
            if lenItemsOnWatchlist > 0:
                print("Deleting %s items from Watchlist." % lenItemsOnWatchlist)
                i = 0
                for tradeID in self.tradeIDs:
                    i += 1
                    try:
                        self.session.watchlistDelete(tradeID)
                        print("({}/{}) Player with TradeID {} deleted from Watchlist.".format(i, lenItemsOnWatchlist,
                                                                                          tradeID))
                    except Exception as error:
                        print(
                            '(Debug) An error in the tradeSearcher has occurred: delete tradeId {} from watchlist: {}'.format(
                                tradeID, error))
                        self.error = True
                self.tradeIDs = []
        elif listTradeIds != None:
            lenItemsTradeIdlist = len(listTradeIds)
            print("Deleting {} items from Watchlist.".format(lenItemsTradeIdlist))
            i = 0
            for tradeID in listTradeIds:
                i += 1
                try:
                    self.session.watchlistDelete(tradeID)
                    print("({}/{}) Player with TradeID {} deleted from Watchlist.".format(i, lenItemsTradeIdlist,
                                                                                          tradeID))
                except Exception as error:
                    print(
                        'Debug An error in the tradeSearcher has occurred: delete tradeId {} from watchlist: {}'.format(
                            tradeID, error))
                    self.error = True
            self.tradeIDs = []
        self.currentState = State.pending
