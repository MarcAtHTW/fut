import imaplib
from bs4 import BeautifulSoup as BS


class PinAutomater:

    def __init__(self, host, user, passw, port=993):
        self.host   = host
        self.user   = user
        self.passw  = passw
        self.port   = port
        self.connetion = None
        self.pin    = None


    def login(self):
        self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        self.connection.login(self.user , self.passw)
        self.connection.list()
        # Out: list of "folders" aka labels in gmail.
        self.connection.select("inbox")  # connect to inbox.

        result, data = self.connection.search(None, "ALL")

        ids = data[0]  #
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, data = self.connection.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        soup = BS(raw_email, 'html.parser')
        bTags = []
        for i in soup.findAll('b'):
            if len(bTags) <= 1:
                bTags.append(i.text)
            elif len(bTags) == 2:
                break
        eaSecurityCode = bTags[1]
        self.pin = eaSecurityCode
        print('Got EA-Security-Code:%s' % eaSecurityCode)
        return self

    def logoff(self):
        self.connection.close()
        self.connection.logout()

    def getPin(self):
        return int(self.pin)