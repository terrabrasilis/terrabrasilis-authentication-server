#!/usr/bin/python3
from configparser import ConfigParser
import os

class ConfigDB:

    #constructor
    def __init__(self, filename='db.cfg', section='database'):
        self.filename = filename
        self.section = section

    def get(self):
        
        config_file = (os.path.dirname(__file__) or '.') + '/config/' + self.filename

        # Test if db.cfg exists
        if not os.path.exists(config_file):
            # get connection params from env vars
            f1 = open(os.getenv('PG_HOST_AUTHENTICATION_SERVER_SECRET'), "r")
            host = f1.read()
            print(host)
            f2 = open(os.getenv('PG_PORT_AUTHENTICATION_SERVER_SECRET'), "r")
            port = f2.read()
            print(port)
            f3 = open(os.getenv('PG_DATABASE_AUTHENTICATION_SERVER_SECRET'), "r")
            database = f3.read()
            print(database)
            f4 = open(os.getenv('PG_USER_AUTHENTICATION_SERVER_SECRET'), "r")
            username = f4.read()
            print(username)
            f5 = open(os.getenv('PG_PASSWORD_AUTHENTICATION_SERVER_SECRET'), "r")
            password = f5.read()
            print(password)
            with open(config_file, "w") as configfile:
                print('[database]', file=configfile)
                print("host={}".format(host), file=configfile)
                print("port={}".format(port), file=configfile)
                print("database={}".format(database), file=configfile)
                print("user={}".format(username), file=configfile)
                print("password={}".format(password), file=configfile)

        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(config_file)
    
        # get section, default to database
        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))
    
        return db