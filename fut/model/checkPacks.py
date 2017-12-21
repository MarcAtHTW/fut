import json


class CheckPacks:

    def __init__(self, fut_session, db):
        self.session = fut_session
        self.db = db


    def packsInDb(self, db):

        items = self.session.packs()

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
        quantityList.clear
        saleTypeList.clear()
        isPremiumList.clear
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
                     descriptionList,
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

        sql = "insert into fut_packs (id, description, coins, quantity, saleType, isPremium, InfoItemQuantity, GoldQuantity, " \
               "SilverQuantity, BronzeQuantity, RareQuantity, points, start, ends) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        for t in x:
            db.insert(sql, t)


