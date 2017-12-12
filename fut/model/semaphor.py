from time import sleep

class Semaphor:

    def __init__(self, fut_session):
        self.isLocked                  = False
        self.session = fut_session


    def search(self, tradeId):
        while self.isLocked == True:
            print('(Searcher): isLocked == True !')
            sleep(1)
        self.isLocked = True
        self.session.sendToWatchlist(int(tradeId))
        self.isLocked = False

    def check(self, tradeId):
        while self.isLocked == True:
            print('(Checker): isLocked == True !')
            sleep(1)
        self.isLocked = True
        self.session.watchlistDelete(tradeId)
        self.isLocked = False