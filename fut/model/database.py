import json
import pymysql
import sys
import fut
from fut.model.watchlist import  Watchlist


def executeSqlFromFile(connection, filename):
    """    Oeffnet sql file, laedt enthaltene SQL-Skripte und fuehrt eines nach dem anderen aus.
    Quelle: https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python

    :param connection
    :param filename
    :rtype: String
    :return Erfolgsmessage
    :raises ValueError: Wenn SQL-Befehl fehlschlaegt
    """
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlfile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlcommands = sqlfile.split(';')

    # Execute every command from the input file

    # This will skip and report errors
    # For example, if the tables do not yet exist, this will skip over
    # the DROP TABLE commands

    for command in sqlcommands:
        connection.query(command)
        # print("Befehl ausgefuehrt: ", command)
    return


def loadPlayerDatabase(coreobject, connection):
    """    Lädt alle FUT-Spieler und schreibt sie in die Tabelle 'fut_players' in der Datenbank

    :param coreobject: fut Core Object
    :param connection: db-connection
    :rtype: String
    :return Erfolgsmessage
    """
    # players = coreobject.players
    # playerdump = json.dumps(players)
    # for key, value in players.items():
    # print(key)
    # print(value)
    #    for k, v in value.items():
    #        print(k)
    #        print(v)
    # print(playerdump)

    players = coreobject.players

    idList = []
    firstnameList = []
    lastnameList = []
    surnameList = []
    ratingList = []
    nationalityList = []

    for key, value in players.items():

        for k, v in value.items():
            if k == "firstname":
                firstnameList.append(v)
            if k == "lastname":
                lastnameList.append(v)
            if k == "id":
                idList.append(v)
            if k == "surname":
                surnameList.append(v)
            if k == "rating":
                ratingList.append(v)
            if k == "nationality":
                nationalityList.append(v)

    # q = "DROP TABLE IF EXISTS `fut_players`; CREATE TABLE IF NOT EXISTS fut_players ( ressourceId VARCHAR(15) NOT NULL, firstname VARCHAR(45) DEFAULT NULL, firstname VARCHAR(45) DEFAULT NULL, firstname VARCHAR(45) DEFAULT NULL, rating INT(3) DEFAULT NULL, nationality INT(3) DEFAULT NULL, PRIMARY KEY (ressourceId)) "
    sql = "insert into fut_players (ressourceId, firstname, lastname, surname, rating, nationality) values (%s, %s, convert(%s using utf8), %s, %s, %s)"

    # Erstellung einer Liste bestehend aus den Listen der Attribute
    x = list(zip(idList, firstnameList, lastnameList, surnameList, ratingList, nationalityList))
    print(x)
    # Einfügung der Liste x in die Datenbank
    for item in x:
        connection.insert(sql, item)

"""Speicherung der Watchlist in der Datenbank mit allen Attributen"""
def succesTradesFromWatchlist(coreobject, connection):

    currentBidList = []
    assetIdList = []
    buyNowPriceList = []
    startingBidList = []
    contractList = []
    fitnessList = []
    timestampList = []
    tradeIdList = []
    idList = []
    offersList = []
    expiresList = []
    sellerEstablishedList = []
    tradeStateList = []
    bidStateList = []
    sellerIdList = []
    sellerNameList = []
    watchedList = []
    time_stampList = []
    ratingList = []
    resourceIdList = []
    itemStateList = []
    rareflagList = []
    formationList = []
    leagueIdList = []
    injuryTypeList = []
    injuryGamesList = []
    lastSalePriceList = []
    trainingList = []
    suspensionList = []
    pos_itionList = []
    playStyleList = []
    discardValueList = []
    itemTypeList = []
    cardTypeList = []
    cardsubtypeidList = []
    ownersList = []
    untradeableList = []
    moraleList = []
    statsList0List = []
    statsList1List = []
    statsList2List = []
    statsList3List = []
    statsList4List = []
    lifetimeStats0List = []
    lifetimeStats1List = []
    lifetimeStats2List = []
    lifetimeStats3List = []
    lifetimeStats4List = []
    attributeList0List = []
    attributeList1List = []
    attributeList2List = []
    attributeList3List = []
    attributeList4List = []
    attributeList5List = []
    teamidList = []
    assistsList = []
    lifetimeAssistsList = []
    loyaltyBonusList = []
    pileList = []
    nationList = []
    ye_arList = []
    resourceGameYearList = []
    cou_ntList = []
    untradeableCountList = []


    for y in coreobject.watchlist():
        #if y["tradeState"] == "closed":
        try:
            gotdata = 'null'
            currentBidList.append(y["currentBid"])
            assetIdList.append(y["assetId"])
            buyNowPriceList.append(y["buyNowPrice"])
            startingBidList.append(y["startingBid"])
            contractList.append(y["contract"])
            fitnessList.append(y["fitness"])
            timestampList.append(y["timestamp"])
            tradeIdList.append(y["tradeId"])
            idList.append(y["id"])
            offersList.append(y["offers"])
            expiresList.append(y["expires"])
            sellerEstablishedList.append(y["sellerEstablished"])
            tradeStateList.append(y["tradeState"])
            bidStateList.append(y["bidState"])
            sellerIdList.append(y["sellerId"])
            sellerNameList.append(y["sellerName"])
            watchedList.append(y["watched"])
            time_stampList.append(y["timestamp"])
            ratingList.append(y["rating"])
            resourceIdList.append(y["resourceId"])
            itemStateList.append(y["itemState"])
            rareflagList.append(y["rareflag"])
            formationList.append(y["formation"])
            leagueIdList.append(y["leagueId"])
            injuryTypeList.append(y["injuryType"])
            injuryGamesList.append(y["injuryGames"])
            lastSalePriceList.append(y["lastSalePrice"])
            trainingList.append(y["training"])
            suspensionList.append(y["suspension"])
            pos_itionList.append(y["position"])
            playStyleList.append(y["playStyle"])
            discardValueList.append(y["discardValue"])
            itemTypeList.append(y["itemType"])
            cardTypeList.append(y["cardType"])
            cardsubtypeidList.append(y["cardsubtypeid"])
            ownersList.append(y["owners"])
            untradeableList.append(y["untradeable"])
            moraleList.append(y["morale"])
            statsList0List.append(y["statsList"][0]["value"])
            statsList1List.append(y["statsList"][1]["value"])
            statsList2List.append(y["statsList"][2]["value"])
            statsList3List.append(y["statsList"][3]["value"])
            statsList4List.append(y["statsList"][4]["value"])
            lifetimeStats0List.append(y["lifetimeStats"][0]["value"])
            lifetimeStats1List.append(y["lifetimeStats"][1]["value"])
            lifetimeStats2List.append(y["lifetimeStats"][2]["value"])
            lifetimeStats3List.append(y["lifetimeStats"][3]["value"])
            lifetimeStats4List.append(y["lifetimeStats"][4]["value"])
            attributeList0List.append(y["attributeList"][0]["value"])
            attributeList1List.append(y["attributeList"][1]["value"])
            attributeList2List.append(y["attributeList"][2]["value"])
            attributeList3List.append(y["attributeList"][3]["value"])
            attributeList4List.append(y["attributeList"][4]["value"])
            attributeList5List.append(y["attributeList"][5]["value"])
            teamidList.append(y["teamid"])
            assistsList.append(y["assists"])
            lifetimeAssistsList.append(y["lifetimeAssists"])
            loyaltyBonusList.append(y["loyaltyBonus"])
            pileList.append(y["pile"])
            nationList.append(y["nation"])
            ye_arList.append(y["year"])
            resourceGameYearList.append(y["resourceGameYear"])
            cou_ntList.append(y["count"])
            untradeableCountList.append(y["untradeableCount"])
            isDataOK = True
        except IndexError as e:
            isDataOK = False
            print("Index Error in database.py: {}".format(e))

    if isDataOK:
        # Erstellung einer Liste bestehend aus den Listen der Attribute
        x = list(zip(tradeIdList, buyNowPriceList, tradeStateList, bidStateList, startingBidList, idList, offersList, currentBidList, expiresList, sellerEstablishedList, sellerIdList, sellerNameList, watchedList, time_stampList,
        ratingList, assetIdList, resourceIdList, itemStateList, rareflagList, formationList, leagueIdList, injuryTypeList, injuryGamesList, lastSalePriceList, fitnessList, trainingList, suspensionList, contractList, pos_itionList, playStyleList, discardValueList, itemTypeList,
                      cardTypeList, cardsubtypeidList, ownersList, untradeableList, moraleList, statsList0List, statsList1List, statsList2List, statsList3List, statsList4List, lifetimeStats0List, lifetimeStats1List, lifetimeStats2List, lifetimeStats3List, lifetimeStats4List,
                      attributeList0List, attributeList1List, attributeList2List, attributeList3List, attributeList4List, attributeList5List, teamidList, assistsList, lifetimeAssistsList, loyaltyBonusList, pileList, nationList, ye_arList, resourceGameYearList, cou_ntList, untradeableCountList))

        sql = "insert into fut_watchlist (tradeId, buyNowPrice, tradeState, bidState, startingBid, id, offers, currentBid, expires, sellerEstablished, sellerId, sellerName, watched, time_stamp, " \
              "rating, assetId, resourceId, itemState, rareflag, formation, leagueId, injuryType, injuryGames, lastSalePrice, fitness, training, suspension, contract, pos_ition, playStyle, discardValue, itemType, " \
                "cardType, cardsubtypeid, owners, untradeable, morale, statsList0, statsList1, statsList2, statsList3, statsList4, lifetimeStats0, lifetimeStats1, lifetimeStats2, lifetimeStats3, lifetimeStats4, " \
               "attributeList0, attributeList1, attributeList2, attributeList3, attributeList4, attributeList5, teamid, assists, lifetimeAssists, loyaltyBonus, pile, nation, ye_ar, resourceGameYear, cou_nt, untradeableCount) " \
               "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Einfügung der Liste x in die Datenbank
        for item in x:
            connection.insert(sql, item)
    elif not isDataOK:
        print("Index Error in database.py. Go ahead..")
        pass

