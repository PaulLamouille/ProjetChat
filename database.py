import sqlite3
from os.path import exists
from datetime import datetime

class Database:

    def __init__(self):
        self.DB_PATH = 'chat_database.db'

        db_exist = exists(self.DB_PATH)
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cur = self.conn.cursor()

        if not db_exist:
            self.cur.execute("create table users(username text primary_key, password text)")
            self.cur.execute("create table log(username text, ip text, date text, cmd text)")

    def add_user(self, username : str, password : str):
        sql = "insert into users(username, password) values (?, ?)"
        self.cur.execute(sql, (username, password))
        self.conn.commit()
    
    def add_log(self, username : str, ip : str, cmd : str):
        sql = "insert into log (username, ip, date, cmd) values (?, ?, ?, ?)"
        self.cur.execute(sql, (username, ip, str(datetime.now()), cmd))
        self.conn.commit()

    def select_user(self, username : str):
        '''
        Return (username, password)\n
        Return None if no user with username
        '''
        sql = "select * from users where username=?;"
        self.cur.execute(sql, (username,))
        reader = self.cur.fetchone()
        if reader is None: return None
        return reader[0],reader[1]

    def select_all_logs(self):
        sql = "select * from log;"
        self.cur.execute(sql)
        reader = self.cur.fetchall()
        return [(row[0], row[1], row[2], row[3]) for row in reader]