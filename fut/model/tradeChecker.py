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
        print('Start: startTradeChecker')

        while anErrorIsReached is False:
            lengthWatchlist = len(self.session.watchlist())
            # Wie lange soll der Bot schlafen, wenn das Objekt null ist?
            if lengthWatchlist == 0:
                print('Kein Item auf der Watchlist, Sleep eine Minute')
                time.sleep(60)
            else:
                itemOfWatchlist = self.session.watchlist()[0]

                if itemOfWatchlist['expires'] != -1:
                    print('Sleep expireTime: '+ str(itemOfWatchlist['expires']))
                    time.sleep(itemOfWatchlist['expires'])

                elif itemOfWatchlist['expires'] == -1:
                    print('Datensatz zur DB senden')
                    self.session.watchlistDelete(itemOfWatchlist['tradeId'])
                    self.safeToDB(itemOfWatchlist)


# SafeToDB, Daten des Trades abgreifen und in die Datenbank speichern
    def safeToDB(self, item):
        print(item)

        sqlItem = [item['tradeId'], item['buyNowPrice'], item['tradeState'], item['bidState'], item['startingBid'], item['id'], item['offers'],
        item['currentBid'], item['expires'], item['sellerEstablished'], item['sellerId'], item['sellerName'], item['watched'], item['timestamp'],
        item['rating'], item['assetId'], item['resourceId'], item['itemState'], item['rareflag'], item['formation'], item['leagueId'],
        item['injuryType'], item['injuryGames'], item['lastSalePrice'], item['fitness'], item['training'], item['suspension'],
        item['contract'], item['position'], item['playStyle'], item['discardValue'], item['itemType'],
        item['cardType'], item['cardsubtypeid'], item['owners'], item['untradeable'], item['morale'], item['statsList'][0]["value"],
        item['statsList'][1]["value"], item['statsList'][2]["value"], item['statsList'][3]["value"], item['statsList'][4]["value"],
        item['lifetimeStats'][0]["value"],item['lifetimeStats'][1]["value"], item['lifetimeStats'][2]["value"], item['lifetimeStats'][3]["value"], item['lifetimeStats'][4]["value"],
        item['attributeList'][0]["value"], item['attributeList'][1]["value"], item['attributeList'][2]["value"], item['attributeList'][3]["value"], item['attributeList'][4]["value"],
        item['attributeList'][5]["value"], item['teamid'], item['assists'], item['lifetimeAssists'], item['loyaltyBonus'], item['pile'],
        item['nation'], item['year'], item['resourceGameYear']]

        sql = "insert into fut_watchlist (tradeId, buyNowPrice, tradeState, bidState, startingBid, id, offers, currentBid, expires, sellerEstablished, sellerId, sellerName, watched, time_stamp, " \
              "rating, assetId, resourceId, itemState, rareflag, formation, leagueId, injuryType, injuryGames, lastSalePrice, fitness, training, suspension, contract, pos_ition, playStyle, discardValue, itemType, " \
              "cardType, cardsubtypeid, owners, untradeable, morale, statsList0, statsList1, statsList2, statsList3, statsList4, lifetimeStats0, lifetimeStats1, lifetimeStats2, lifetimeStats3, lifetimeStats4, " \
              "attributeList0, attributeList1, attributeList2, attributeList3, attributeList4, attributeList5, teamid, assists, lifetimeAssists, loyaltyBonus, pile, nation, ye_ar, resourceGameYear) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        print(sqlItem)

        # Einfügung der Liste x in die Datenbank
        self.db.insert(sql, sqlItem)



