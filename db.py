import sqlite3, os
import pymysql

from typing import List, Tuple
from settings import db_host, db_port, db_user, db_password, db_name, categories_table
from loguru import logger


class DataBaseHandler:
    def __init__(self):
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()

        # Проверка и создание отсутствующих таблицы
        logger.debug('Checking the om "viewed_links" table')
        mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS viewed_links (
        url	VARCHAR(200) NOT NULL UNIQUE)""")

        mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
        name VARCHAR(50),
        value VARCHAR(30) NOT NULL,
        PRIMARY KEY(name))""")

        logger.debug('Checking the om "stopwords" table')
        mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS stopwords (
        word VARCHAR(200) NOT NULL)""")

        # self.mysql_cursor.execute("""
        # CREATE TABLE IF NOT EXISTS watchlist (
        # url	VARCHAR(200) NOT NULL UNIQUE,
        # price NUMERIC)""")

        logger.debug('Checking the om "categories" table')
        mysql_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {categories_table} (
        url	VARCHAR(255) NOT NULL UNIQUE)""")

        logger.debug('Checking the om "users" table')
        mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        chat_id	VARCHAR(50) NOT NULL,
        PRIMARY KEY(chat_id))""")

        logger.debug('Checking the om "blacklist" table')
        mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS blacklist (
        seller_id	VARCHAR(200) NOT NULL,
        PRIMARY KEY(seller_id))""")

        logger.debug('Checking the om "min_prices" table')
        mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS min_prices (
        url	VARCHAR(200) NOT NULL UNIQUE,
        min_price INT,
        PRIMARY KEY(url))""")

        logger.debug('Initialization of settings')
        try:
            mysql_cursor.execute("INSERT INTO settings (name, value) VALUES ('delay', '1')")
            mysql_cursor.execute("INSERT INTO settings (name, value) VALUES ('interval', '600')")
            mysql_connection.commit()

        except pymysql.err.IntegrityError:
            pass

        logger.info('DataBaseHandler - ready!')

    def _get_connection_and_cursor(self):
        logger.debug('Сonnecting to a remote database')
        mysql_connection = pymysql.connect(host=db_host,
                                           port=db_port,
                                           user=db_user,
                                           password=db_password,
                                           database=db_name,
                                           charset='utf8mb4')
        mysql_cursor = mysql_connection.cursor()
        mysql_connection.autocommit(True)

        return mysql_connection, mysql_cursor

    def get_viewed_links(self) -> List:
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()
        logger.debug('Getting viewed links')
        while True:
            try:
                mysql_cursor.execute("SELECT url FROM viewed_links")
                resp = mysql_cursor.fetchall()
            except pymysql.err.OperationalError:
                mysql_connection.ping(True)

            else:
                break
        logger.debug('Viewed links received')
        return [d[0] for d in resp]

    def add_to_viewed_links(self, url: str):
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()
        logger.debug(f'Adding to viewed links - {url}')
        while True:
            try:
                mysql_cursor.execute("INSERT INTO viewed_links VALUES(%s)", (url,))
                mysql_connection.commit()
            except pymysql.err.OperationalError:
                mysql_connection.ping(True)

            except pymysql.err.IntegrityError:
                break
            else:
                break
        logger.debug('The url has been added to viewed links')

    def update_delay(self, delay):
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()
        logger.debug('Updating the delay')
        try:
            float(delay)
        except ValueError:
            raise ValueError

        else:
            delay = str(delay)

            mysql_cursor.execute('UPDATE settings SET value = ? WHERE name = "delay"', (delay,))

        logger.debug('The delay has been updated')

    def get_categories(self) -> List:
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()
        logger.debug('Getting categories')
        mysql_cursor.execute(f"SELECT url FROM {categories_table}")
        resp = mysql_cursor.fetchall()
        logger.debug('Categories received')
        return [d for d in resp]

    def get_blacklist(self) -> List:
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()
        logger.debug('Getting blacklist')
        mysql_cursor.execute("SELECT seller_id FROM blacklist")
        resp = mysql_cursor.fetchall()

        return [d[0] for d in resp]

    def get_stopwords(self) -> List:
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()
        logger.debug('Getting stopwords')
        mysql_cursor.execute("SELECT word FROM stopwords")
        resp = mysql_cursor.fetchall()

        return [d[0] for d in resp]

    def get_min_price_by_url(self, url):
        mysql_connection, mysql_cursor = self._get_connection_and_cursor()
        logger.debug(f'Getting min price by url - {url}')
        mysql_cursor.execute("SELECT min_price FROM min_prices WHERE url = ?", (url,))
        resp = mysql_cursor.fetchone()
        logger.debug(f'Min price: {resp} for {url}')
        return resp

if __name__ == '__main__':
    db = DataBaseHandler()
    print(db.get_categories())
