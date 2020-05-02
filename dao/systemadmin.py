from config.dbconfig import pg_config
import psycopg2


class SysAdmDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllSysAdm(self):
        cursor = self.conn.cursor()
        query = "select * from sys_adm;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSysAdmById(self, said):
        cursor = self.conn.cursor()
        query = "select * from sys_adm where said = %s;"
        cursor.execute(query, (said,))
        result = cursor.fetchone()
        return result

    def getSysAdmnByUsername(self, sausername):
        cursor = self.conn.cursor()
        query = "select * from sys_adm where sausername = %s;"
        cursor.execute(query, (sausername,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getUserBySysAdmId(self, said):
        cursor = self.conn.cursor()
        query = "select uid, ufirstname, ulastname from users natural inner join sys_adm where said = %s;"
        cursor.execute(query, (said,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, sausername):
        cursor = self.conn.cursor()
        query = "insert into sys_adm(sausername) values (%s) returning said;"
        cursor.execute(query, (sausername,))
        said = cursor.fetchone()[0]
        self.conn.commit()
        return said

    def update(self, said, sausername):
        cursor = self.conn.cursor()
        query = "update sys_adm set sausername = %s where said = %s;"
        cursor.execute(query, (sausername, said,))
        self.conn.commit()
        return said

    def delete(self, said):
        cursor = self.conn.cursor()
        query = "delete from sys_adm where said = %s;"
        cursor.execute(query, (said,))
        self.conn.commit()
        return said
