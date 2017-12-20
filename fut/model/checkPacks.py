import json


class CheckPacks:

    def __init__(self, fut_session, db, isPackChecker):
        self.session = fut_session
        self.db = db
        self.isPackChecker = isPackChecker


    def lookForPacks(self):
        items = self.session.packs()
        print(items)