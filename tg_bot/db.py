import sqlite3

from tg_bot import config


class DataBaseManager:
    def __init__(self, database=config.DB_NAME):
        self.connection = sqlite3.connect(database)
        
        self.cursor = self.connection.cursor()

    def add_user(self, id_user, first_name, nick_name):
        self.cursor.execute(
            f'''INSERT INTO users (id_user, first_name, nickname) VALUES
            ({id_user}, '{first_name}', '{nick_name}');'''
        )
        self.connection.commit()

    def get_user(self, id_user):
        self.cursor.execute(
            f'''SELECT id_user, first_name, nickname FROM users WHERE 
            id_user = {id_user};'''
        )
        is_exists = self.cursor.fetchone()
        self.connection.close
        
        return str(is_exists)
