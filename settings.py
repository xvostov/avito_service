# from configparser import ConfigParser
import os
from loguru import logger

logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation='1 day')

# config = ConfigParser()
# config.read('data/settings.ini')

user_agent = os.getenv('user_agent')
bot_api_token = os.getenv('bot_api_token')
telegram_api_address = os.getenv('telegram_api_address')
# interaval = os.getenv('interval')

# Database
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host = os.getenv('db_host')
db_port = int(os.getenv('db_port'))
db_name = os.getenv('db_name')
categories_table = os.getenv('categories_table').strip()


# user_agent = config['App']['user_agent']
# bot_api_token = config['Telegram']['bot_api_token']
# telegram_api_address = config['Telegram']['telegram_api_address']
# interaval = config['App']['interval']
#
# # Database
# db_user = config['Database']['db_user']
# db_password = config['Database']['db_password']
# db_host = config['Database']['db_host']
# db_port = int(config['Database']['db_port'])
# db_name = config['Database']['db_name']
# categories_table = config['Database']['categories_table'].strip()
