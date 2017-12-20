import configparser
import os

class Credentials:

    def __init__(self):
        self.ea             = {}
        self.db             = {}
        self.mail           = {}
        self.slack          = {}
        self.loadCredentialsFromMyCredentials()


    def loadCredentialsFromMyCredentials(self):
        """ Lädt die Zugangsdaten für die Datenbank + Anmeldung bei EA + E-Mail für den Pinautomater.

        :rtype: Dictionary
        :return credentials: Zugangsdaten EA + DB
        """
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../model', 'mycredentials.conf'))

        credentials = {
            "DB_Host": config.get("configuration-DB", "host"),
            "DB_User": config.get("configuration-DB", "user"),
            "DB_Pass": config.get("configuration-DB", "pass"),
            "DB_Name": config.get("configuration-DB", "db"),
            "EA_Mail": config.get("configuration-EA", "mail"),
            "EA_Pass": config.get("configuration-EA", "pass"),
            "EA_Secr": config.get("configuration-EA", "secret"),
            "MAIL_Host": config.get("configuration-MAIL-IMAP", "host"),
            "MAIL_User": config.get("configuration-MAIL-IMAP", "user"),
            "MAIL_Pass": config.get("configuration-MAIL-IMAP", "pass"),
            "MAIL_Port": config.get("configuration-MAIL-IMAP", "port"),
            "SLACK_TOKEN": config.get("configuration - SLACK", "slack_token")
        }

        self.db['host'] = credentials['DB_Host']
        self.db['user'] = credentials['DB_User']
        self.db['pass'] = credentials['DB_Pass']
        self.db['name'] = credentials['DB_Name']

        self.ea['mail'] = credentials['EA_Mail']
        self.ea['pass'] = credentials['EA_Pass']
        self.ea['secr'] = credentials['EA_Secr']

        self.mail['host'] = credentials['MAIL_Host']
        self.mail['user'] = credentials['MAIL_User']
        self.mail['pass'] = credentials['MAIL_Pass']
        self.mail['port'] = credentials['MAIL_Port']

        self.slack['slack_token'] = credentials['SLACK_TOKEN']