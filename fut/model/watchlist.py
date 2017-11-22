import json

class Watchlist:

    tradeIDs = []
    items = []

    def __init__(self, fut_session):
        self.session                    = fut_session
        self.tradepile                  = fut_session.tradepile()
        self.unassigned                 = fut_session.unassigned()
        #self.club                       = fut_session.club(count=10, level=10, type=1, start=0)
        #self.clubConsumablesDetails     = fut_session.clubConsumableDetails()
        self.length                     = len(fut_session.watchlist())

    def fillup(self, resultsetTransfermarketsearch, maxLengthOfWatchlist=50):
        """ Fills up Watchlist with items found at a market search.
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
        """ Clears the current watchlist.
        :type listTradeIds: list
        :param listTradeIds: List of tradeIDs. Can be used to manually delete items from watchlist.
        """
        if listTradeIds == None:
            self.loadTradeIdsFromLiveWatchlist()
            for tradeID in self.tradeIDs:
                self.session.watchlistDelete(tradeID)
                print("Player with TradeID %s deleted from Watchlist." % tradeID)
            self.tradeIDs = []
        elif listTradeIds != None:
            for tradeID in listTradeIds:
                self.session.watchlistDelete(tradeID)
                print("Player with TradeID %s deleted from Watchlist. (Manual via TradeID-List)" % tradeID)
            self.tradeIDs = []

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
        """

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

"""
>>> session.sendToTradepile(item_id)                         # add card to tradepile
>>> session.sendToClub(trade_id, item_id)                    # add card to club
>>> session.sendToWatchlist(trade_id)                        # add card to watchlist
>>> session.tradepileDelete(trade_id)                        # removes item from tradepile
>>> session.watchlistDelete(trade_id)                        # removes item from watch list (you can pass single str/ing or list/tuple of ids - like in quickSell)
"""