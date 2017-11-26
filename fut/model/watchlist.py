import json
from datetime import datetime
from fut.model.enumeration import State

class Watchlist:

    tradeIDs = []
    items = []
    currentState = State.pending


    def __init__(self, fut_session):
        self.session                    = fut_session
        self.tradepile                  = fut_session.tradepile()
        #self.unassigned                 = fut_session.unassigned()
        #self.club                       = fut_session.club(count=10, level=10, type=1, start=0)
        #self.clubConsumablesDetails     = fut_session.clubConsumableDetails()
        self.length                     = len(fut_session.watchlist())
        self.expire                     = {}

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
        """ Clears the current watchlist.
        :type listTradeIds: list
        :param listTradeIds: List of tradeIDs. Can be used to manually delete items from watchlist.
        """
        if listTradeIds == None:
            self.loadTradeIdsFromLiveWatchlist()
            lenItemsOnWatchlist = len(self.tradeIDs)
            print("Deleting %s items from Watchlist." % lenItemsOnWatchlist)
            i = 0
            for tradeID in self.tradeIDs:
                i+=1
                self.session.watchlistDelete(tradeID)
                print("({}/{}) Player with TradeID {} deleted from Watchlist.".format(i, lenItemsOnWatchlist, tradeID))
            self.tradeIDs = []
        elif listTradeIds != None:
            lenItemsTradeIdlist = len(self.listTradeIds)
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


    def sendItemsToWatchlistWithMinExpireTime(self, minExpireTimeInMinutes, count, assetId):
        """ Sends items to watchlist using min expire time in munites, count of players and assetId.
        :type minExpireTimeInMinutes: int
        :type count: int
        :type assetId: int
        :param minExpireTimeInMinutes: Minimum expiretime in minutes.
        :param count: Count of items.
        :param assetId: Item asset-id.
        """
        self.currentState = State.search
        minExpireTimeInSeconds = minExpireTimeInMinutes * 60
        itemsWithMinExpireTime = []

        page_size = 48
        while len(itemsWithMinExpireTime) < count:
            #items_resultset = self.session.searchAuctions(ctype='player', page_size=page_size)
            items_resultset = self.session.searchAuctions(ctype='player', assetId=assetId, page_size=page_size)
            for item in items_resultset:
                if item['expires'] > minExpireTimeInSeconds:
                    if count > 0:
                        itemsWithMinExpireTime.append(item)
                        count -= 1
            page_size += 1
        self.expire['minExpireTimeInMinutes']   = minExpireTimeInMinutes
        self.expire['created']                  = datetime.now()

        print("Sending {} items to watchlist.".format(len(itemsWithMinExpireTime)))
        i = 0
        lenItemsWithMinExpireTime = len(itemsWithMinExpireTime)
        for item in itemsWithMinExpireTime:
            i += 1
            tradeID = item['tradeId']
            self.session.sendToWatchlist(tradeID)
            print("({}/{}) Player with TradeID {} added to Watchlist.".format(i, lenItemsWithMinExpireTime, tradeID))
        self.setExpiretime()
        self.currentState = State.pending


    def setExpiretime(self):
        """ Sets the max Expiretime of current watchlist items getting from current session."""
        itemsOfWatchlist    = self.session.watchlist()
        maxExpiretime       = 0

        for item in itemsOfWatchlist:
            if item['expires'] > maxExpiretime:
                maxExpiretime = item['expires']
        self.expire['expires'] = maxExpiretime

    def getExpiretime(self):
        """ Gets the max Expiretime of current watchlist items.
        :rtype: int
        :return: Expiretime in minutes.
        """
        return self.expire['expires'] / 60



"""
>>> session.sendToTradepile(item_id)                         # add card to tradepile
>>> session.sendToClub(trade_id, item_id)                    # add card to club
>>> session.sendToWatchlist(trade_id)                        # add card to watchlist
>>> session.tradepileDelete(trade_id)                        # removes item from tradepile
>>> session.watchlistDelete(trade_id)                        # removes item from watch list (you can pass single str/ing or list/tuple of ids - like in quickSell)
"""