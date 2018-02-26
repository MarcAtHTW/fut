import time
import datetime

class CheckPacks:

    def __init__(self, fut_session, db, isPackSearcher, threadStatus):
        """
        Construktor of the tradecheacker.
        :param fut_session: valid fut session
        :param db: for saving SBC's
        :param isPackSearcher: boolean to handle the entrance
        :param threadStatus: class to controll the threads
        """

        self.session = fut_session
        self.db = db
        self.isPackSearcher = isPackSearcher
        self.anErrorHasOccured = False
        self.threadStatus = threadStatus
        self.timestamp = 0


    def packsInFUT(self):
        """
        This method loads current fut packs and stores this to DB.        
        """

        print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
              '] ### CheckPacks started ###')
        time.sleep(10)
        while self.anErrorHasOccured is False:
            if self.threadStatus.getCheckerStatus() is True and self.threadStatus.getSearcherStatus() is True:

                try:
                    if int(time.time()) >= self.timestamp:
                        print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                              '] CheckPacks: Packs werden abgerufen.')
                        items = self.session.packs()
                        self.savePacksInDB(items)
                        self.timestamp = int(time.time()) + 1800

                except Exception as error:
                    print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                          '] {Debug} An error in the CheckPacks has occurred: ', error)

            else:
                self.anErrorHasOccured = True

    def savePacksInDB(self, items):
        """
        Saves packs to DB.
        !! Important, the order of which the attributes are appended to the list is crucial !!
        :param items: list of items
        :return:
        """

        idList = []
        descriptionList = []
        coinsList = []
        pointsList = []
        quantityList =[]
        saleTypeList = []
        isPremiumList = []
        packContentInfoItemQuantityList = []
        packContentGoldQuantityList = []
        packContentSilverQuantityList = []
        packContentBronzeQuantityList = []
        packContentRareQuantityList = []
        startList = []
        endList = []

        idList.clear()
        descriptionList.clear()
        coinsList.clear()
        quantityList.clear()
        saleTypeList.clear()
        isPremiumList.clear()
        packContentInfoItemQuantityList.clear()
        packContentGoldQuantityList.clear()
        packContentSilverQuantityList.clear()
        packContentBronzeQuantityList.clear()
        packContentRareQuantityList.clear()
        startList.clear()
        endList.clear()
        pointsList.clear()

        for y in items["purchase"]:
            idList.append(y["id"])
            descriptionList.append(y["description"])
            quantityList.append(y["quantity"])
            saleTypeList.append(y["saleType"])
            isPremiumList.append(y["isPremium"])
            packContentInfoItemQuantityList.append(y["packContentInfo"]["itemQuantity"])
            packContentGoldQuantityList.append(y["packContentInfo"]["goldQuantity"])
            packContentSilverQuantityList.append(y["packContentInfo"]["silverQuantity"])
            packContentBronzeQuantityList.append(y["packContentInfo"]["bronzeQuantity"])
            packContentRareQuantityList.append(y["packContentInfo"]["rareQuantity"])
            coinsList.append(y["coins"])

            if "fifaCashPrice" in y:
                pointsList.append(y["fifaCashPrice"])
            else:
                pointsList.append("0")

            if "start" in y:
                startList.append(y["start"])
            else:
                startList.append("0")

            if "end" in y:
                endList.append(y["end"])
            else:
                endList.append("0")

        x = list(zip(idList,
                     coinsList,
                     quantityList,
                     saleTypeList,
                     isPremiumList,
                     packContentInfoItemQuantityList,
                     packContentGoldQuantityList,
                     packContentSilverQuantityList,
                     packContentBronzeQuantityList,
                     packContentRareQuantityList,
                     pointsList,
                     startList,
                     endList))

        z = list(zip(idList, descriptionList))

        sql = "insert into fut_packs (id, coins, quantity, saleType, isPremium, InfoItemQuantity, GoldQuantity, " \
               "SilverQuantity, BronzeQuantity, RareQuantity, points, start, ends) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        sql_main = "insert into fut_desc (id, description) values (%s, %s)"

        for t in x:
            self.db.insert(sql, t)

        for d in z:
            self.db.insert(sql_main, d)

        print('[', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
              '] CheckPacks: Packs were stored in DB.')



