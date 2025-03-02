import locale
import os

from dotenv import load_dotenv

load_dotenv()

if os.name == 'nt':
    locale.setlocale(locale.LC_ALL, '')  # для WINDOWS
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # для UNIX


class Config(object):

    FASTAPI_URL = 'http://localhost:5000'

