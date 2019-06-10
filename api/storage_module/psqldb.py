#!/usr/bin/python3
import psycopg2
from storage_module.configdb import ConfigDB
from storage_module.app_exceptions import ConnectionError, QueryError

class PsqlDB:
    
    def __init__(self):
        # read connection parameters
        try:
            conf = ConfigDB()
            self.params = conf.get()
        except Exception as configError:
            raise configError

    def connect(self):
        self.conn = None
        self.cur = None
        try:
            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(**self.params)
            self.cur = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            raise ConnectionError('Missing connection:', error)
    
    def close(self):
        # close the communication with the PostgreSQL
        if self.cur is not None:
            self.cur.close()
            self.cur = None
        # disconnect from the PostgreSQL server
        if self.conn is not None:
            self.conn.close()

    def commit(self):
        # disconnect from the PostgreSQL server
        if self.conn is not None:
            # commit the changes
            self.conn.commit()
    
    def rollback(self):
        # disconnect from the PostgreSQL server
        if self.conn is not None:
            # commit the changes
            self.conn.rollback()

    def execQuery(self, query):
        try:
            
            if self.cur is None:
                self.cur.open()
                raise ConnectionError('Missing cursor:', 'Has no valid database cursor ({0})'.format(query))
            # execute a statement
            self.cur.execute(query)

        except (Exception, psycopg2.DatabaseError) as error:
            self.rollback()
            raise QueryError('Query execute issue', error)
        except (BaseException) as error:
            self.rollback()
            raise QueryError('Query execute issue', error)
            

    def fetchData(self, query):
        data = None
        try:
            # execute a statement
            self.execQuery(query)
            # retrive data
            data = self.cur.fetchall()
            
        except QueryError as error:
            raise error
            
        return data