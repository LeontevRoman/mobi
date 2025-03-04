import locale
import os

from dotenv import load_dotenv

load_dotenv()

if os.name == 'nt':
    locale.setlocale(locale.LC_ALL, '')  # для WINDOWS
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # для UNIX

use_docker = os.environ.get('USE_DOCKER', 'False').lower() == 'true'

class Config(object):

    FASTAPI_HOST = os.environ.get('FASTAPI_HOST', 'localhost')
    FASTAPI_PORT = os.environ.get('FASTAPI_PORT', '5000')
