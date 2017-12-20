import time
import datetime

class ThreadStatus:

    def __init__(self):
        self.isSearcherAlive                   = True
        self.isCheckerAlive                    = True


    def getSearcherStatus(self):
        return self.isSearcherAlive

    def getCheckerStatus(self):
        return self.isCheckerAlive


    def setSearcherStatus(self, status):
        self.isSearcherAlive = status
        print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] ThreadStatus: Searcher-Status changed to: {}'.format(self.isSearcherAlive))

    def setCheckerStatus(self, status):
        self.isCheckerAlive = status
        print('[',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'] ThreadStatus: Checker-Status changed to: {}'.format(self.isCheckerAlive))