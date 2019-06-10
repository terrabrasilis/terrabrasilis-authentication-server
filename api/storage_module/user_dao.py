#!/usr/bin/python3
from storage_module.psqldb import PsqlDB
from storage_module.app_exceptions import DatabaseError, MissingParameterError
import datetime
from storage_module.user import User

# The User Data Access Object handles all interactions with the user table.
class UserDao:

    #constructor
    def __init__(self):
        self.db = PsqlDB()

    def storeUser(self, email, password, admin=False):
        """
        Start insert process to store a user into user table

        @param email, The user email to registry
        @param password, The associated password
        @param admin, The admin information. Default is false.
        
        Return id value or, in error, raise a DatabaseError exception.
        
        Warning: This method opens connection, run the process and close connection.
        """

        id = None
        try:
            self.db.connect()
            id = self.__insert(email, password, admin)
            self.db.commit()

        except BaseException as error:
            raise error
        finally:
            self.db.close()

        return id

    def getUserBy(self, filter):
        """
        Get one user by filter.
        If the filter is a string instance them the filtered attribute is email
        otherwise it uses the id on where clause.
        """
        user = None
        try:
            self.db.connect()
            user = self.__selectBy(filter)
        except BaseException as error:
            raise error
        finally:
            self.db.close()

        return user
    
    def __selectBy(self, where_filter):
        """
        Fetch one user from database
        """
        user=None
        term = "email='"+where_filter+"'" if isinstance(where_filter, str) else "id="+str(where_filter)

        sql = "SELECT id, email, password, registered_on, verified, admin "
        sql += "FROM public.user "
        sql += "WHERE {0}".format(term)

        data = self.db.fetchData(sql)
        if data and data[0]:
            user = User(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5])

        return user

    def __insert(self, email, password, admin):
        """
        Store input data into user table...
        """
        registered_on = datetime.datetime.now()
        admin = ('t' if admin else 'f')
        verified = 'f'

        sql = "INSERT INTO public.user"
        sql += "(email, password, registered_on, verified, admin) "
        sql += "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(email, password, registered_on, verified, admin)
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