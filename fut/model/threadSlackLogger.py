import time

class ThreadSlackLogger:

    def __init__(self, tCheck, tSearch, slack_client, botName):
        self.threadChecker                  = tCheck
        self.threadSearcher                 = tSearch
        self.slack_client                   = slack_client
        self.botName                        = botName
        self.allThreadsCounter              = 0
        self.oneThreadCounter                 = 0


    def ckeckThreads(self):
        print('### ThreadSlackLogger started ###')

        andErrorHasOccured = False
        while andErrorHasOccured is False:
            if self.threadChecker.isAlive() == False and self.threadSearcher.isAlive() == False:
                # print('SlackLogger: all Bots are not alive')
                self.allThreadsCounter += 1
                time.sleep(60)
                if self.allThreadsCounter == 3:
                    print('SlackLogger: all Bots are not alive')
                    self.slack_client.api_call("chat.postMessage", channel='C8FQ2E0F8',
                                          text=self.botName+'<!channel|> IMPORTANT: No thread is running!!!.',
                                          username='pythonbot')
                    time.sleep(3600)
                    self.allThreadsCounter = 0
            else:
                self.allThreadsCounter -= 1

            if (self.threadChecker.isAlive() == True and self.threadSearcher.isAlive() == False) or (
                            self.threadChecker.isAlive() == False and self.threadSearcher.isAlive() == True):
                self.oneThreadCounter += 1
                time.sleep(60)
                if self.oneThreadCounter == 3:
                    print('SlackLogger: all Bots are not alive')
                    self.slack_client.api_call("chat.postMessage", channel='C8FQ2E0F8',
                                               text=self.botName + '<!channel|> IMPORTANT: One Thread is running!!! Checker: '+self.threadChecker+', Searcher: '+self.threadSearcher,
                                               username='pythonbot')
                    time.sleep(3600)
                    self.oneThreadCounter = 0
            else:
                self.oneThreadCounter -= 1






