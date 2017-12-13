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

    def setCheckerStatus(self, status):
        self.isCheckerAlive = status