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
        print('ThreadStatus: Searcher-Status changed to: {}'.format(self.isSearcherAlive))

    def setCheckerStatus(self, status):
        self.isCheckerAlive = status
        print('ThreadStatus: Checker-Status changed to: {}'.format(self.isCheckerAlive))