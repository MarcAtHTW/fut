import time

class ThreadSlackLogger:

    def __init__(self, tCheck, tSearch, slack_client):
        self.threadChecker                  = tCheck
        self.threadSearcher                 = tSearch
        self.slack_client                    = slack_client


    def ckeckThreads(self):
        print('### ThreadSlackLogger started ###')

        andErrorHasOccured = False
        while andErrorHasOccured is False:
            if self.threadChecker.isAlive() == False and self.threadSearcher.isAlive() == False:
                time.sleep(30)
                if self.threadChecker.isAlive() == False and self.threadSearcher.isAlive() == False:
                    print('SlackLogger: all Bots are not alive')
                    self.slack_client.api_call("chat.postMessage", channel='C8FQ2E0F8',
                                          text='<!channel|> IMPORTANT: No thread is running!!!.',
                                          username='pythonbot')
                    time.sleep(200)
            elif (self.threadChecker.isAlive() == True and self.threadSearcher.isAlive() == False) or (
                            self.threadChecker.isAlive() == False and self.threadSearcher.isAlive() == True):
                time.sleep(30)
                if (self.threadChecker.isAlive() == True and self.threadSearcher.isAlive() == False) or (
                            self.threadChecker.isAlive() == False and self.threadSearcher.isAlive() == True):
                    print('SlackLogger: Only one Bot is alive')
                    self.slack_client.api_call("chat.postMessage", channel='C8FQ2E0F8',
                                               text='<!channel|> IMPORTANT: Only one Bot is alive!!!.',
                                               username='pythonbot')
                    time.sleep(200)




