# from configparser import ConfigParser
import os
from loguru import logger

logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation='1 day')


user_agent = os.getenv('user_agent')
bot_api_token = os.getenv('bot_api_token')
telegram_api_address = os.getenv('telegram_api_address')
# interaval = os.getenv('interval')

MIN_PRICE = os.getenv('min_price')
ALLOWED_CATEGORIES = [category.lower() for category in os.getenv('ALLOWED_CATEGORIES').split(',')]

# Database
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host = os.getenv('db_host')
db_port = int(os.getenv('db_port'))
db_name = os.getenv('db_name')
categories_table = os.getenv('categories_table').strip()

# Prometheus
prom_exp_port = os.getenv('prom_exp_port')