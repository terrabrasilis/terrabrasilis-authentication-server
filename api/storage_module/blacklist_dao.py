#!/usr/bin/python3
from storage_module.psqldb import PsqlDB
from storage_module.app_exceptions import DatabaseError, MissingParameterError
import datetime

# The Blacklist Data Access Object handles all interactions with the blacklist table.
class BlacklistDao:

    #constructor
    def __init__(self):
        self.db = PsqlDB()

    def storeToken(self, token):
        """
        Start insert process to store a token into Blacklist table

        @param token, The user token to logout

        Return id value or, in error, raise a DatabaseError exception.
        
        Warning: This method opens connection, run the process and close connection.
        """

        id = None
        try:
            self.db.connect()
            id = self.__insert(token)
            self.db.commit()

        except BaseException as error:
            raise error
        finally:
            self.db.close()

        return id

    def tokenIsBlacklisted(self, token):
        """
        Check if one token is invalid.
        Assumes the token as invalid by default.
        @return boolean False if the token is not in blacklist otherwise returns True
        """
        invalid = True
        try:
            sql = "SELECT 'True' as invalid "
            sql += "FROM public.blacklist_token "
            sql += "WHERE token='{0}'".format(token)

            self.db.connect()
            data = self.db.fetchData(sql)
            invalid = (True if data and data[0][0]=='True' else False)

        except BaseException as error:
            raise error
        finally:
            self.db.close()

        return invalid
    
    def __insert(self, token):
        """
        Store input data into blacklist table...
        """
        blacklisted_on = datetime.datetime.now()

        sql = "INSERT INTO public.blacklist_token( "
        sql += "token, blacklisted_on) "
        sql += "VALUES ('{0}', '{1}')".format(token, blacklisted_on)
        sql += " RETURNING id"

        self.__basicExecute(sql)

        id_of_new_row = self.db.cur.fetchone()[0]
        return id_of_new_row

    def __basicExecute(self, sql):
        """
        Execute a basic SQL statement.
        """
        try:
            self.db.execQuery(sql)
        except Exception as error:
            self.db.rollback()
            raise DatabaseError('Database error:', error)