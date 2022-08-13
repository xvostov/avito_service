import sqlite3, os
import pymysql

from typing import List, Tuple
from settings import db_host, db_port,db_user, db_password, db_name, categories_table
from loguru import logger

class DataBaseHandler:
    def __init__(self):
        logger.debug('Сonnecting to a remote database')
        self.mysql_connection = pymysql.connect(host=db_host,
                                                port=db_port,
                                                user=db_user,
                                                password=db_password,
                                                database=db_name,
                                                charset='utf8mb4')
        self.mysql_cursor = self.mysql_connection.cursor()
        self.mysql_connection.autocommit(True)
        
        # Проверка и создание отсутствующих таблицы
        logger.debug('Checking the om "viewed_links" table')
        self.mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS viewed_links (
        url	VARCHAR(200) NOT NULL UNIQUE)""")



        self.mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
        name VARCHAR(50),
        value VARCHAR(30) NOT NULL,
        PRIMARY KEY(name))""")

        logger.debug('Checking the om "stopwords" table')
        self.mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS stopwords (
        word VARCHAR(200) NOT NULL)""")

        # self.mysql_cursor.execute("""
        # CREATE TABLE IF NOT EXISTS watchlist (
        # url	VARCHAR(200) NOT NULL UNIQUE,
        # price NUMERIC)""")


        logger.debug('Checking the om "categories" table')
        self.mysql_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {categories_table} (
        url	VARCHAR(255) NOT NULL UNIQUE)""")

        logger.debug('Checking the om "users" table')
        self.mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        chat_id	VARCHAR(50) NOT NULL,
        PRIMARY KEY(chat_id))""")

        logger.debug('Checking the om "blacklist" table')
        self.mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS blacklist (
        seller_id	VARCHAR(200) NOT NULL,
        PRIMARY KEY(seller_id))""")


        logger.debug('Initialization of settings')
        try:
            self.mysql_cursor.execute("INSERT INTO settings (name, value) VALUES ('delay', '1')")
            self.mysql_cursor.execute("INSERT INTO settings (name, value) VALUES ('interval', '600')")
            self.mysql_connection.commit()

        except pymysql.err.IntegrityError:
            pass

        logger.info('DataBaseHandler - ready!')

    def get_viewed_links(self) -> List:
        logger.debug('Getting viewed links')
        while True:
            try:
                self.mysql_cursor.execute("SELECT url FROM viewed_links")
                resp = self.mysql_cursor.fetchall()
            except pymysql.err.OperationalError:
                self.mysql_connection.ping(True)

            else:
                break
        logger.debug('Viewed links received')
        return [d[0] for d in resp]

    def add_to_viewed_links(self, url: str):
        logger.debug(f'Adding to viewed links - {url}')
        while True:
            try:
                self.mysql_cursor.execute("INSERT INTO viewed_links VALUES(%s)", (url,))
                self.mysql_connection.commit()
            except pymysql.err.OperationalError:
                self.mysql_connection.ping(True)

            except pymysql.err.IntegrityError:
                break
            else:
                break
        logger.debug('The url has been added to viewed links')

    def update_delay(self, delay):
        logger.debug('Updating the delay')
        try:
            float(delay)
        except ValueError:
            raise ValueError

        else:
            delay = str(delay)

        while True:
            try:
                self.mysql_cursor.execute('UPDATE settings SET value = ? WHERE name = "delay"', (delay, ))
                self.mysql_connection.commit()
            except pymysql.err.OperationalError:
                self.mysql_connection.ping(True)
            else:
                break
        logger.debug('The delay has been updated')

    def get_categories(self) -> List:
        self.mysql_connection.ping(True)

        logger.debug('Getting categories')
        self.mysql_cursor.execute(f"SELECT url FROM {categories_table}")
        resp = self.mysql_cursor.fetchall()
        logger.debug('Categories received')
        return [d for d in resp]

    def get_blacklist(self) -> List:
        self.mysql_connection.ping(True)

        logger.debug('Getting blacklist')
        self.mysql_cursor.execute("SELECT seller_id FROM blacklist")
        resp = self.mysql_cursor.fetchall()

        return [d[0] for d in resp]

    def get_stopwords(self) -> List:
        self.mysql_connection.ping(True)
        logger.debug('Getting stopwords')
        self.mysql_cursor.execute("SELECT word FROM stopwords")
        resp = self.mysql_cursor.fetchall()

        return [d[0] for d in resp]

if __name__ == '__main__':
    db = DataBaseHandler()
    print(db.get_categories())