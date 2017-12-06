from fut.model.enumeration import State


class TradeSearcher:
    def __init__(self, fut_session, assetIds, minExpireTime, maxExpireTimeinMinutes):
        self.assetId = 0
        self.assetIds = assetIds
        self.minExpireTimeInMinutes = minExpireTime
        self.maxExpireTimeinMinutes = maxExpireTimeinMinutes
        self.session = fut_session
        self.tradepile = fut_session.tradepile()
        self.length = len(fut_session.watchlist())
        self.expire = {}
        self.currentState = State.pending
        self.watchlist = fut_session.watchlist()

    def startTradeSearcher(self):
        print('### TradeSearcher started ###')
