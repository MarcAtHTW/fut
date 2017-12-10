from fut.model.enumeration import State
import time

class TradeChecker:
    def __init__(self, fut_session, db):
        self.session        = fut_session
        self.db             = db
        self.length         = len(fut_session.watchlist())
        self.expire         = {}
        self.currentState   = State.wait
        self.watchlist      = fut_session.watchlist()



# watchliste abrufen und items nach abgelaufenen Objekten suchen. (expires ist dann auf -1)
# wenn expired dann def SaveToDB
    def startTradeChecker(self):
        anErrorIsReached = False
        print('### TradeChecker started ###')

        while anErrorIsReached is False:
            try:
                lengthWatchlist = len(self.session.watchlist())
            except Exception as error:
                print('{Debug} An error in the tradeChecker has occurred: session.watchlist() failed: ', error)
            # Wie lange soll der Bot schlafen, wenn das Objekt null ist?
            if lengthWatchlist == 0:
                print('Kein Item auf der Watchlist, Sleep eine Minute')
                time.sleep(60)
            else:
                try:
                    itemOfWatchlist = self.session.watchlist()[0]

                    if itemOfWatchlist['expires'] != -1:
                        print('Sleep expireTime: ' + str(itemOfWatchlist['expires']))
                        time.sleep(itemOfWatchlist['expires'])

                    elif itemOfWatchlist['expires'] == -1:
                        print('Datensatz zur DB senden')
                        self.session.watchlistDelete(itemOfWatchlist['tradeId'])
                        self.saveToDB(itemOfWatchlist)
                except Exception as error:
                    print('{Debug} An error in the tradeChecker while-loop has occurred: ', error)



# SafeToDB, Daten des Trades abgreifen und in die Datenbank speichern

    def saveToDB(self, item):
        """
        Saves the actual item into the db table fut_watchlist.
        !! Important, the order of which the attributes are appended to the list is crucial !!
        :param item: the least expired trade on the watchlist
        :return:
        """
        # print(item)

        sqlItem = []
        y = item
        isDataOK = False
        try:
            gotdata = 'null'
            sqlItem.append(y["tradeId"])
            sqlItem.append(y["buyNowPrice"])
            sqlItem.append(y["tradeState"])
            sqlItem.append(y["bidState"])
            sqlItem.append(y["startingBid"])
            sqlItem.append(y["id"])
            sqlItem.append(y["offers"])
            sqlItem.append(y['currentBid'])
            sqlItem.append(y["expires"])
            sqlItem.append(y["sellerEstablished"])
            sqlItem.append(y["sellerId"])
            sqlItem.append(y["sellerName"])
            sqlItem.append(y["watched"])
            sqlItem.append(y["timestamp"])
            sqlItem.append(y["rating"])
            sqlItem.append(y["assetId"])
            sqlItem.append(y["resourceId"])
            sqlItem.append(y["itemState"])
            sqlItem.append(y["rareflag"])
            sqlItem.append(y["formation"])
            sqlItem.append(y["leagueId"])
            sqlItem.append(y["injuryType"])
            sqlItem.append(y["injuryGames"])
            sqlItem.append(y["lastSalePrice"])
            sqlItem.append(y["fitness"])
            sqlItem.append(y["training"])
            sqlItem.append(y["suspension"])
            sqlItem.append(y["contract"])
            sqlItem.append(y["position"])
            sqlItem.append(y["playStyle"])
            sqlItem.append(y["discardValue"])
            sqlItem.append(y["itemType"])
            sqlItem.append(y["cardType"])
            sqlItem.append(y["cardsubtypeid"])
            sqlItem.append(y["owners"])
            sqlItem.append(y["untradeable"])
            sqlItem.append(y["morale"])
            if 'statsList' in y:
                sqlItem.append(y["statsList"][0]["value"])
                sqlItem.append(y["statsList"][1]["value"])
                sqlItem.append(y["statsList"][2]["value"])
                sqlItem.append(y["statsList"][3]["value"])
                sqlItem.append(y["statsList"][4]["value"])
            if 'lifetimeStats' in y:
                sqlItem.append(y["lifetimeStats"][0]["value"])
                sqlItem.append(y["lifetimeStats"][1]["value"])
                sqlItem.append(y["lifetimeStats"][2]["value"])
                sqlItem.append(y["lifetimeStats"][3]["value"])
                sqlItem.append(y["lifetimeStats"][4]["value"])
            if 'attributeList' in y:
                sqlItem.append(y["attributeList"][0]["value"])
                sqlItem.append(y["attributeList"][1]["value"])
                sqlItem.append(y["attributeList"][2]["value"])
                sqlItem.append(y["attributeList"][3]["value"])
                sqlItem.append(y["attributeList"][4]["value"])
                sqlItem.append(y["attributeList"][5]["value"])
            sqlItem.append(y["teamid"])
            sqlItem.append(y["assists"])
            sqlItem.append(y["lifetimeAssists"])
            sqlItem.append(y["loyaltyBonus"])
            sqlItem.append(y["pile"])
            sqlItem.append(y["nation"])
            sqlItem.append(y["year"])
            sqlItem.append(y["resourceGameYear"])
            # cou_ntList.append(y["count"])
            # untradeableCountList.append(y["untradeableCount"])
            isDataOK = True
        except IndexError as e:
            isDataOK = False
            print("Index Error in database.py: {}".format(e))

        if isDataOK:
            sql = "insert into fut_watchlist (tradeId, buyNowPrice, tradeState, bidState, startingBid, id, offers, currentBid, expires, sellerEstablished, sellerId, sellerName, watched, time_stamp, " \
                  "rating, assetId, resourceId, itemState, rareflag, formation, leagueId, injuryType, injuryGames, lastSalePrice, fitness, training, suspension, contract, pos_ition, playStyle, discardValue, itemType, " \
                  "cardType, cardsubtypeid, owners, untradeable, morale, statsList0, statsList1, statsList2, statsList3, statsList4, lifetimeStats0, lifetimeStats1, lifetimeStats2, lifetimeStats3, lifetimeStats4, " \
                  "attributeList0, attributeList1, attributeList2, attributeList3, attributeList4, attributeList5, teamid, assists, lifetimeAssists, loyaltyBonus, pile, nation, ye_ar, resourceGameYear) " \
                  "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # Einfügung der Liste x in die Datenbank
            self.db.insert(sql, sqlItem)
            print('trade {} saved to db'.format(item["tradeId"]))
        elif not isDataOK:
            pass
