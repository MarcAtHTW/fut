from fut.model.enumeration import State
import time

class TradeChecker:
    def __init__(self, fut_session, db):
        self.session        = fut_session
        self.db             = db
        self.length         = len(fut_session.watchlist())
        self.expire         = {}
        self.currentState   = State.wait
        self.watchlist      = fut_session.watchlist()



# watchliste abrufen und items nach abgelaufenen Objekten suchen. (expires ist dann auf -1)
# wenn expired dann def SaveToDB
    def startTradeChecker(self):
        andErrorIsReached = False

        while andErrorIsReached is True:
            itemOfWatchlist = self.session.watchlist()[0]
            print(itemOfWatchlist)
            if itemOfWatchlist['expires'] != -1:
                print(itemOfWatchlist['expires'])
                time.sleep(itemOfWatchlist['expires'])

            elif itemOfWatchlist['expires'] == -1:
                self.safeToDB(itemOfWatchlist)
                self.session.watchlistDelete(itemOfWatchlist['TradeID'])


           # for item in itemsOfWatchlist:
            #    if item['expires'] > maxExpiretime:
             #       maxExpiretime = item['expires']
            # self.expire['expires'] = maxExpiretime


# fut.watchlistDelete(trade_id)

# SafeToDB, Daten des Trades abgreifen und in die Datenbank speichern
    def safeToDB(self,item):
        print(item)





