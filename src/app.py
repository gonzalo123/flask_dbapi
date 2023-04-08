import logging

from flask import Flask
from flask_compress import Compress

from lib.logger import setup_logging
from lib.utils import CustomJSONEncoder
from modules.example import blueprint as example
from settings import LOG_LEVEL, ELK_APP, ELK_INDEX, ELK_PROCESS, LOG_PATH

logging.basicConfig(level=LOG_LEVEL)

setup_logging(app=ELK_APP,
              index=ELK_INDEX,
              process=ELK_PROCESS,
              log_path=LOG_PATH)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
compress = Compress()
compress.init_app(app)

app.register_blueprint(example)
