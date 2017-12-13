from time import sleep

class Semaphor:

    def __init__(self, fut_session):
        self.isLocked                   = False
        self.whoLocked                  = ()
        self.session                    = fut_session


    def search(self, tradeId):
        while self.isLocked == True:
            if self.whoLocked == 'Searcher':
                self.isLocked = False
            else:
                print('(Searcher): isLocked == True ! von: {}'.format(self.whoLocked))
                sleep(1)

        self.isLocked = True
        self.whoLocked = 'Searcher'

        try:
            self.session.sendToWatchlist(int(tradeId))
            self.isLocked = False
            return False
        except Exception as error:
            print('{Debug} An error in the semaphore def search has occurred: ', error)
            self.isLocked = False
            return True

    def check(self, tradeId):
        while self.isLocked == True:
            if self.whoLocked == 'Checker':
                self.isLocked = False
            else:
                print('(Checker): isLocked == True ! von: {}'.format(self.whoLocked))
                sleep(1)

        self.isLocked = True
        self.whoLocked = 'Checker'

        try:
            self.session.watchlistDelete(tradeId)
            self.isLocked = False
            return False
        except Exception as error:
            print('{Debug} An error in the semaphore def check has occurred: ', error)
            self.isLocked = False
            return True