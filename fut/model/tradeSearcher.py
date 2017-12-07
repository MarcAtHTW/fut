from fut.model.enumeration import State
import time


class TradeSearcher:
    def __init__(self, fut_session, assetIds, minExpireTime, maxExpireTimeinMinutes):
        self.assetId = 0
        self.assetIds = assetIds
        self.minExpireTimeInMinutes = minExpireTime
        self.maxExpireTimeinMinutes = maxExpireTimeinMinutes
        self.session = fut_session
        self.tradepile = fut_session.tradepile()
        self.length = len(fut_session.watchlist())
        self.watchlistSize = fut_session.watchlist_size
        self.expire = {}
        self.tradeIDs = []
        self.currentState = State.pending
        self.watchlist = fut_session.watchlist()
        # numberOfPlayers Attribut evtl. benötigt, alternativ könnte es agil zur Laufzeit abgefragt werden: session.wathlist_size
        self.numberOfPlayers = 50

    def startTradeSearcher(self):
        print('### TradeSearcher started ###')
        """ Clear Watchlist at startup. """
        # self.clear()
        while True:
            for assetId in self.assetIds:
                print('(Debug): Current ressource ID: {}'.format(assetId))
                self.assetId = assetId
                """ Search Trades for current assetId"""
                self.searchAsset(self.minExpireTimeInMinutes, self.maxExpireTimeinMinutes, assetId)

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

        self.currentState = State.search
        items_resultset = self.session.searchAuctions(ctype='player', assetId=assetId, start=currentPage, page_size=25)

        print('{} From Page {}'.format(self.currentState, currentPage))
        self.currentState = State.chooseTrades
        for item in items_resultset:
            if item['expires'] > minExpireTimeInSeconds and item[
                'expires'] < maxExpireTimeInSeconds and tradeCounter <= 5:
                self.saveToWatchlist(item['tradeId'])
                tradeCounter += 1
            else:
                noNewTradeCounter += 1
            if tradeCounter >= 5 or noNewTradeCounter >= 10:
                break
        print('tradeCounter: ', tradeCounter)
        print('noNewTradeCounter: ', noNewTradeCounter)


    def getIdsFromPage(self, page):
        """ Gets all ID's from Current Resultset.
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
        self.length = len(self.session.watchlist())
        self.currentState = State.watchTrades

        print('trades on watchlist: ', self.length)

        self.loadTradeIdsFromLiveWatchlist()
        while tradeId not in self.tradeIDs:
            if self.length < self.watchlistSize:
                try:
                    self.session.sendToWatchlist(int(tradeId))
                    print("Player with TradeID {} added to Watchlist.".format(tradeId))
                except Exception as error:
                    print(error)
                    self.startTradeSearcher()
                break
            else:
                print('No free slot on Watchlist. Waiting for 2 sec.')
                time.sleep(2)
                self.length = len(self.session.watchlist())

    def loadTradeIdsFromLiveWatchlist(self):
        """ Gets the current live Trade-IDs from watchlist and loads it into local property tradeIDs
        :rtype: list
        :return:  live Trade-IDs from watchlist.
        """
        tradeIds = []
        resultset = self.session.watchlist()
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
                    self.session.watchlistDelete(tradeID)
                    print("({}/{}) Player with TradeID {} deleted from Watchlist.".format(i, lenItemsOnWatchlist,
                                                                                          tradeID))
                self.tradeIDs = []
        elif listTradeIds != None:
            lenItemsTradeIdlist = len(listTradeIds)
            print("Deleting {} items from Watchlist.".format(lenItemsTradeIdlist))
            i = 0
            for tradeID in listTradeIds:
                i += 1
                self.session.watchlistDelete(tradeID)
                print("({}/{}) Player with TradeID {} deleted from Watchlist.".format(i, lenItemsTradeIdlist, tradeID))
            self.tradeIDs = []
        self.currentState = State.pending
