import os
from logging import INFO
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

APP_ID = 'dbapi'
APP_PATH = 'dbapi'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

load_dotenv(dotenv_path=Path(BASE_DIR).resolve().joinpath('env', ENVIRONMENT, '.env'))

PROCESS_ID = os.getenv('PROCESS_ID', APP_ID)
LOG_LEVEL = os.getenv('LOG_LEVEL', INFO)
ELK_APP = f'{APP_ID}.{PROCESS_ID}'
ELK_INDEX = f'{APP_ID}_{ENVIRONMENT}'
ELK_PROCESS = APP_ID
LOG_PATH = f'./logs/{APP_ID}.log'

BEARER = os.getenv('BEARER')

# Database configuration
DEFAULT = 'default'

DATABASES = {
    DEFAULT: f"dbname='{os.getenv('DEFAULT_DB_NAME')}' user='{os.getenv('DEFAULT_DB_USER')}' host='{os.getenv('DEFAULT_DB_HOST')}' password='{os.getenv('DEFAULT_DB_PASS')}' port='{os.getenv('DEFAULT_DB_PORT')}'"
}
