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
        """ Gives access to your Mailbox. Define credentials in fut/model/mycredentials.conf section "MAIL-IMAP".
        Returns IMAP4-SSL-Connection represents your mailbox.
        :rtype:     PinAutomater
        :return:    IMAP4_SSL-Connection
        """
        self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        self.connection.login(self.user , self.passw)
        self.connection.list()
        self.connection.select("inbox")
        return self

    def loadSecurityCodeFromMailbox(self):
        """ Fishs the needle/securityCode out of the heap/mailbox/soupe.
        Returns IMAP4-SSL-Connection represents your mailbox.
        :rtype:     PinAutomater
        :return:    IMAP4_SSL-Connection
        """
        result, data = self.connection.search(None, "ALL")
        ids = data[0]
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
        """ Closes the IMAP4-SSL-Connection."""
        self.connection.close()
        self.connection.logout()

    def getPin(self):
        """ Gets the current EA-Security-Code send via Mail.
        :rtype:     int
        :return:    EA-Security-Code
        """
        return int(self.pin)