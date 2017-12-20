from time import sleep
import time
import datetime

class Semaphor:

    def __init__(self, fut_session, slack_client, botName):
        self.isLocked                   = False
        self.whoLocked                  = ()
        self.session                    = fut_session
        self.slack_client               = slack_client
        self.botName                    = botName

    def search(self, tradeId):
        while self.isLocked == True:
            if self.whoLocked == 'Searcher':
                self.isLocked = False
            else:
                sleep(1)

        self.isLocked = True
        self.whoLocked = 'Searcher'

        try:
            self.session.sendToWatchlist(int(tradeId))
            self.isLocked = False
            return False
        except Exception as error:
            print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] {Debug} An error in the semaphore def search has occurred: ', error)

            self.isLocked = False
            if str(error) == '' or str(error) == ' ':
                return False
            else:
                return True

    def check(self, tradeId):
        while self.isLocked == True:
            if self.whoLocked == 'Checker':
                self.isLocked = False
            else:
                sleep(1)

        self.isLocked = True
        self.whoLocked = 'Checker'

        try:
            self.session.watchlistDelete(tradeId)
            self.isLocked = False
            return False
        except Exception as error:
            print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] {Debug} An error in the semaphore def check has occurred: ', error)
            self.isLocked = False
            if str(error) == '' or str(error) == ' ':
                return False
            else:
                return True