from time import sleep

class Semaphor:

    def __init__(self, fut_session):
        self.isLocked                  = False
        self.whoLocked                 = ()
        self.session = fut_session


    def search(self, tradeId):
        while self.isLocked == True:
            if self.isLocked == True:
                print('(Searcher): isLocked == True ! von: {}'.format(self.whoLocked))
                sleep(1)
            elif self.whoLocked == 'search':
                self.isLocked = False

        self.isLocked = True
        self.whoLocked = 'search'
        self.session.sendToWatchlist(int(tradeId))
        self.isLocked = False

    def check(self, tradeId):
        while self.isLocked == True:
            if self.isLocked == True:
                print('(Checker): isLocked == True ! von: {}'.format(self.whoLocked))
                sleep(1)
            elif self.whoLocked == 'check':
                self.isLocked = False

        self.isLocked = True
        self.whoLocked = 'check'
        self.session.watchlistDelete(tradeId)
        self.isLocked = False