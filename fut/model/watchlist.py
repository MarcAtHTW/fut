import json

class Watchlist:

    tradeIDs = []

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
        tradeIds = []
        resultset = self.session.watchlist()
        for item in resultset:
            tradeIds.append(item['tradeId'])
        self.tradeIDs = tradeIds
        return self.tradeIDs

"""
>>> session.sendToTradepile(item_id)                         # add card to tradepile
>>> session.sendToClub(trade_id, item_id)                    # add card to club
>>> session.sendToWatchlist(trade_id)                        # add card to watchlist
>>> session.tradepileDelete(trade_id)                        # removes item from tradepile
>>> session.watchlistDelete(trade_id)                        # removes item from watch list (you can pass single str/ing or list/tuple of ids - like in quickSell)
"""