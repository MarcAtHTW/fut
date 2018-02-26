import time
import datetime

class CheckSBC:

    def __init__(self, fut_session, db, isPackSearcher, threadStatus):
        self.session = fut_session
        self.db = db
        self.isPackSearcher = isPackSearcher
        self.threadStatus = threadStatus
        self.anErrorHasOccured = False
        self.timestamp = 0

    def sbcsInFut(self):
        print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
              '] ### CheckSBCs started ###')

        while self.anErrorHasOccured is False:
            if self.threadStatus.getCheckerStatus() is True and self.threadStatus.getSearcherStatus() is True:

                try:
                    if int(time.time()) >= self.timestamp:
                        print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                              '] CheckSBCs: SBCs werden abgerufen.')
                        items = self.session.sbsSets()
                        self.categoriesSBCtoDB(items)
                        self.SBCtoDB(items)
                        self.timestamp = int(time.time()) + 1800

                except Exception as error:
                    print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                          '] {Debug} An error in the CheckSBCs has occurred: ', error)

            else:
                self.anErrorHasOccured = True

    def categoriesSBCtoDB(self, items):

        categoriesList = []
        nameList = []

        categoriesList.clear()
        nameList.clear()

        for y in items["categories"]:

            categoriesList.append(y["categoryId"])
            nameList.append(y["name"])

        x = list(zip(categoriesList, nameList))

        sql = "insert into fut_SBC_categories (id, name) values (%s, %s)"

        for t in x:
            self.db.insert(sql, t)


    def SBCtoDB(self, items):

        setIdList = []
        nameList = []
        categoryIdList = []
        descriptionList = []
        repeatableList = []
        challengesCompletedCountList = []
        endTimeList = []
        awardsisUntradeableList = []
        awardsloanList = []
        itemDataAssetIdList = []
        awardsIdList = []

        setIdList.clear()
        nameList.clear()
        categoryIdList.clear()
        descriptionList.clear()
        repeatableList.clear()
        challengesCompletedCountList.clear()
        endTimeList.clear()
        awardsisUntradeableList.clear()
        awardsloanList.clear()
        itemDataAssetIdList.clear()
        awardsIdList.clear()

        for y in items["categories"]:
            for a in y["sets"]:
                setIdList.append(a["setId"])
                nameList.append(a["name"])
                categoryIdList.append(a["categoryId"])
                descriptionList.append(a["description"])
                repeatableList.append(a["repeatable"])
                challengesCompletedCountList.append(a["challengesCompletedCount"])
                endTimeList.append(a["endTime"])
                for b in a["awards"]:
                    awardsIdList.append(b["value"])
                    awardsisUntradeableList.append(b["isUntradeable"])
                    awardsloanList.append(b["loan"])

        x = list(zip(setIdList,
        nameList,
        categoryIdList,
        descriptionList,
        repeatableList,
        challengesCompletedCountList,
        endTimeList,
        awardsisUntradeableList,
        awardsloanList,
        awardsIdList))

        sql = "insert into fut_SBC (setId, name, categoryId, description, repeatable, challengesCompletedCount, endTime," \
              "isUntradeable, loan, Id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        for t in x:
            self.db.insert(sql, t)

        print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
              '] CheckSBCs: SBCs wurden in DB gespeichert.')