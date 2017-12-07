import json
from datetime import datetime
from fut.model.enumeration import State
from fut.model.database import succesTradesFromWatchlist
import time

class Watchlist:

    tradeIDs = []
    items = []

    def __init__(self, fut_session, db, assetIds, minExpireTime, maxExpireTimeinMinutes, numberOfPlayers):
        self.assetId                    = 0
        self.assetIds                   = assetIds
        self.db                         = db
        self.minExpireTimeInMinutes     = minExpireTime
        self.maxExpireTimeinMinutes     = maxExpireTimeinMinutes
        self.numberOfPlayers            = numberOfPlayers
        self.session                    = fut_session
        self.tradepile                  = fut_session.tradepile()
        #self.unassigned                 = fut_session.unassigned()
        #self.club                       = fut_session.club(count=10, level=10, type=1, start=0)
        #self.clubConsumablesDetails     = fut_session.clubConsumableDetails()
        self.length                     = len(fut_session.watchlist())
        self.expire                     = {}
        self.currentState               = State.pending
        self.watchlist                  = fut_session.watchlist()
        self.isExpired                  = False

    def startBot(self):
        print('### Bot started ###')
        while True:
            for assetId in self.assetIds:
                print('(Debug): Current ressource ID: {}'.format(assetId))
                self.assetId = assetId
                self.printCurrentStateToConsole()
                """ Clear Watchlist at startup. """
                self.clear()

                """ Fill up Watchlist """
                self.sendItemsToWatchlistWithMinExpireTime(self.minExpireTimeInMinutes, self.maxExpireTimeinMinutes,
                                                           self.numberOfPlayers, self.assetId)

                """ Wait expiretime """
                self.setExpiretime()
                expireTime = self.getExpiretime()
                self.setCurrentState(State.wait)
                print("Watchlist expires in {} minutes.".format(expireTime / 60, ))
                currentTime = time.strftime("%H:%M:%S")
                print("Current time: {}".format(currentTime))
                self.waitExpiretime()
                self.isExpired = False
                """ Save Trades """
                self.setCurrentState(State.saveTrades)
                self.printCurrentStateToConsole()
                succesTradesFromWatchlist(self.session, self.db)
                self.setCurrentState(State.pending)

    def fillup(self, resultsetTransfermarketsearch, maxLengthOfWatchlist=50):
        """ Fills up Watchlist with items found at a market search.
        :param numberOfPlayerToSendToWatchlist:
        :type resultsetTransfermarketsearch: list
        :param resultsetTransfermarketsearch: Items of transfer market.
        :type maxLengthOfWatchlist: int
        :param maxLengthOfWatchlist: Max lenght of items possible to put on Watchlist
        """
        i = 0
        self.loadTradeIdsFromLiveWatchlist()
        currentLengthOfWatchlist = len(self.tradeIDs)
        numberOfRequiredPlayers = maxLengthOfWatchlist - currentLengthOfWatchlist

        print("Getting %s players.." % numberOfRequiredPlayers)
        while i < numberOfRequiredPlayers:
            tradeID = resultsetTransfermarketsearch[i]["tradeId"]
            item_id = resultsetTransfermarketsearch[i]["id"]
            self.session.sendToWatchlist(int(tradeID))
            #self.tradeIDs.append(tradeID)
            # fut.sendToWatchlist(x["tradeId"])
            # watchlist = fut.watchlist()
            # print(str(x))
            # print(watchlist)
            i += 1
            print("Added Player No %s ID:%s  to Watchlist" % (i, tradeID))

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
                    i+=1
                    self.session.watchlistDelete(tradeID)
                    print("({}/{}) Player with TradeID {} deleted from Watchlist.".format(i, lenItemsOnWatchlist, tradeID))
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

    def loadItemsFromLiveWatchlist(self):
        """ Gets the current live Trade-IDs from watchlist and loads it into local property tradeIDs
        :rtype: list
        :return:  live items from watchlist.
        """
        resultset = self.session.watchlist()
        self.items = resultset
        return self.items

    def getWatchlistInJsonPrettyPrint(self):
        """ Returns the current Watchlist in a json pretty print string.
        :rtype: str
        :return: Watchlist in json pretty print
        """
        resultset = self.session.watchlist()
        prettyJsonWatchlist = json.dumps(resultset, indent=4, sort_keys=True)
        return prettyJsonWatchlist


    def getPlayerWithMaxExpireTime(self):
        """ Gets the player who stays longest time at watchlist.
        Active items on Watchlost are required.

        :return:
        """
        playerWithMaxExpireTime_ID       = 0
        playerWithMaxExpireTime_TradeID  = 0
        maxExpireTime                    = 0

        resultset = self.session.watchlist()
        for item in resultset:
            if item['expires'] > maxExpireTime:
                maxExpireTime                       = item['expires']
                playerWithMaxExpireTime_ID          = item['id']
                playerWithMaxExpireTime_TradeID     = item['tradeId']

        return playerWithMaxExpireTime_ID, playerWithMaxExpireTime_TradeID

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

    def sendItemsToWatchlistWithMinExpireTime(self, minExpireTimeInMinutes, maxExpireTimeinMinutes, numberOfPlayers,
                                              assetId):
        # ToDo: Methode verschlanken!
        """ Sends items to watchlist using min expire time in minutes, count of players and assetId.
        :type minExpireTimeInMinutes: int
        :type numberOfPlayers: int
        :type assetId: int
        :param minExpireTimeInMinutes: Minimum expiretime in minutes.
        :param numberOfPlayers: Count of items.
        :param assetId: Item asset-id.
        """
        self.currentState = State.search
        print(self.currentState)
        minExpireTimeInSeconds = minExpireTimeInMinutes * 60
        maxExpireTimeInSeconds = maxExpireTimeinMinutes * 60
        itemsWithMinExpireTime = []

        currentPage = 1
        isLastPageReached = False
        isResultsetFull = False
        isNextPageFilledWithNewItems = False
        tradeFound = False
        listTradeIds = []
        resultsetPreviousPage = {}
        listIdsPreviousPage = []
        listIdsCurrentPage = []
        diff = 0
        noNewTradeCounter = 0

        self.currentState = State.chooseTrades
        while isResultsetFull is False and noNewTradeCounter <= 2 and isLastPageReached is False:

            if len(itemsWithMinExpireTime) < numberOfPlayers:
                # items_resultset = self.session.searchAuctions(ctype='player', page_size=page_size)
                items_resultset = self.session.searchAuctions(ctype='player', assetId=assetId, start=currentPage,
                                                              page_size=25)
                listIdsCurrentPage = self.getIdsFromPage(items_resultset)
                if len(listIdsPreviousPage) > 0:
                    diff = set(listIdsCurrentPage) - set(listIdsPreviousPage)
                    # diff = set(listIdsCurrentPage) - set(listIdsPreviousPage)
                    print(listIdsPreviousPage)
                    print(listIdsCurrentPage)
                    print(diff)
                if len(listIdsPreviousPage) == 0:
                    resultsetPreviousPage = items_resultset
                    listIdsPreviousPage = self.getIdsFromPage(resultsetPreviousPage)
                    isNextPageFilledWithNewItems = True
                elif len(diff) > 0:
                    isNextPageFilledWithNewItems = True
                    listIdsPreviousPage = listIdsCurrentPage
                elif len(diff) == 0:
                    isNextPageFilledWithNewItems = False

                # print(self.currentState)
                print('{} From Page {}'.format(self.currentState, currentPage))
                for item in items_resultset:
                    # Choose trades with min expire time, max expire time hardcoded = 10 Minutes = 600 Seconds and has a (not active: current bid.
                    if item['expires'] > minExpireTimeInSeconds and item['expires'] < maxExpireTimeInSeconds:
                        if len(itemsWithMinExpireTime) < numberOfPlayers and item['tradeId'] not in listTradeIds:
                            itemsWithMinExpireTime.append(item)
                            listTradeIds.append(item['tradeId'])
                            tradeFound = True
                            # print(listTradeIds)
                            print('items found: ', len(itemsWithMinExpireTime))
                        else:
                            tradeFound = False
                if tradeFound == True:
                    noNewTradeCounter = 0
                else:
                    noNewTradeCounter += 1
                    print('noNewTradeCounter: ', noNewTradeCounter)

                currentPage += 1
                if isNextPageFilledWithNewItems == False:
                    isLastPageReached = True
            elif len(itemsWithMinExpireTime) == numberOfPlayers:
                isResultsetFull = True

        self.expire['minExpireTimeInMinutes'] = minExpireTimeInMinutes
        self.expire['created'] = datetime.now()

        print("Sending {} items to watchlist.".format(len(itemsWithMinExpireTime)))
        i = 0
        lenItemsWithMinExpireTime = len(itemsWithMinExpireTime)
        for item in itemsWithMinExpireTime:
            i += 1
            tradeID = item['tradeId']
            # print("(Debug: TradeID {} will be added to Watchlist.".format(tradeID))
            try:
                self.session.sendToWatchlist(int(tradeID))
            except Exception as error:
                # self.session.logger("Houston, we have a %s", "bit of a problem", exc_info=1)
                print(error)
                self.startBot()
            print("({}/{}) Player with TradeID {} added to Watchlist.".format(i, lenItemsWithMinExpireTime, tradeID))
        self.currentState = State.pending
        print(self.currentState)


    def setExpiretime(self):
        """ Sets the max Expiretime of current watchlist items getting from current session."""
        itemsOfWatchlist    = self.session.watchlist()
        maxExpiretime       = -1

        for item in itemsOfWatchlist:
            if item['expires'] > maxExpiretime:
                maxExpiretime = item['expires']
        self.expire['expires'] = maxExpiretime

    def getExpiretime(self):
        """ Gets the max Expiretime of current watchlist items.
        :rtype: int
        :return: Expiretime in seconds.
        """
        return self.expire['expires']

    def setCurrentState(self, state):
        """ Sets current watchlist state.
        :type state: State
        :param state: Current state. E.g.: pending, delete, choose...
        """
        if isinstance(state, State):
            self.currentState = state

    def getCurrentState(self):
        """ Sets current watchlist state
        :return: Current state. E.g.: pending, delete, choose...
        """
        return self.currentState

    def printCurrentStateToConsole(self):
        """ Prints current state to console.
        """
        currentState = self.currentState
        print(currentState)

    def waitExpiretime(self):
        """ Waits expiretime. Checks current state and waits till items are expired.
        """
        self.setExpiretime()
        expiretime = self.getExpiretime()
        if expiretime < 0:
            self.isExpired = True
        if self.isExpired == False:
            print('New bid! Waiting.. {} seconds.'.format(expiretime))
            time.sleep(expiretime)
        while self.isExpired == False:
            self.waitExpiretime()



"""
>>> session.sendToTradepile(item_id)                         # add card to tradepile
>>> session.sendToClub(trade_id, item_id)                    # add card to club
>>> session.sendToWatchlist(trade_id)                        # add card to watchlist
>>> session.tradepileDelete(trade_id)                        # removes item from tradepile
>>> session.watchlistDelete(trade_id)                        # removes item from watch list (you can pass single str/ing or list/tuple of ids - like in quickSell)
"""