

class CheckSBC:

    def __init__(self, fut_session, db):
        self.session = fut_session
        self.db = db


    def lookForSBCs(self):
        items = self.session.sbsSets()

    def categoriesSBCtoDB(self,db):

        items = self.session.sbsSets()

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
            db.insert(sql, t)


    def SBCtoDB(self, db):

        items = self.session.sbsSets()

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

                #if "itemData" in a:
 #               if "itemData" in y["sets"]:
 #                   itemDataAssetIdList.append(a["itemData"]["assetId"])
                #else:
                #    itemDataAssetIdList.append("0")

 #       print(itemDataAssetIdList)

        x = list(zip(setIdList,
        nameList,
        categoryIdList,
        descriptionList,
        repeatableList,
        challengesCompletedCountList,
        endTimeList,
        awardsisUntradeableList,
        awardsloanList,
        itemDataAssetIdList,
        awardsIdList))

        sql = "insert into fut_SBC (setId, name, categoryId, description, repeatable, challengesCompletedCount, endTime," \
              "isUntradeable, loan, assetId, Id ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        for t in x:
            db.insert(sql, t)



