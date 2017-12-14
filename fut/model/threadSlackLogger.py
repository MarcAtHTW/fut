class ThreadSlackLogger:

    def __init__(self, threadChecker, threadSearcher, slack_client):
        self.threadChecker                  = threadChecker
        self.threadSearcher                 = threadSearcher
        self.slack_client                    = slack_client


    def ckeckThreads(self):
        andErrorHasOccured = False
        while andErrorHasOccured is True:
            if self.threadChecker.isAlive == False and self.threadSearcher.isAlive ==False:
                self.slack_client.api_call("chat.postMessage", channel='C7HCNTXFF',
                                      text='Test message out of Slack @Channel',
                                      username='pythonbot',
                                      icon_emoji=':ninja:')

