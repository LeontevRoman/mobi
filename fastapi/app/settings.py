import locale
import os

from dotenv import load_dotenv

load_dotenv()

if os.name == 'nt':
    locale.setlocale(locale.LC_ALL, '')  # для WINDOWS
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # для UNIX


class Config(object):

    # Database set
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')


