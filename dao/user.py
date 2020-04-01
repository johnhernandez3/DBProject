# -*- coding: utf-8 -*-
from config.dbconfig import pg_config
import psycopg2

class UserDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllUser(self):
        cursor = self.conn.cursor()
        query = "select * from user;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserById(self, uid):
            cursor = self.conn.cursor()
            query = "select * from user where uid = %s;"
            cursor.execute(query, (uid,))
            result = cursor.fetchone()
            return result

    def getUserByFirstname(self, ufirstname):
        cursor = self.conn.cursor()
        query = "select * from user where ufirstname = %s;"
        cursor.execute(query, (ufirstname,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getUserByLastname(self, ulastname):
        cursor = self.conn.cursor()
        query = "select * from user where ulastname = %s;"
        cursor.execute(query, (ulastname,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getUserByFirstnameandLastname(self, ufirstname, ulastname):
        cursor = self.conn.cursor()
        query = "select * from user where ufirstname = %s and ulastname = %s;"
        cursor.execute(query, (ufirstname, ulastname))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getCompanyByUserId(self, uid):
       cursor = self.conn.cursor()
       query = "select compid, compname from company natural inner join user where uid = %s;"
       cursor.execute(query, (uid,))
       result = []
       for row in cursor:
           result.append(row)
       return result

    def insert(self, ufirstname, ulastname):
        cursor = self.conn.cursor()
        query = "insert into user(ufirstname, ulastname) values (%s, %s) returning uid;"
        cursor.execute(query, (ufirstname, ulastname))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid