import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger import jsonlogger

DEFAULT_FROM = 'appbeat'


class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, app, process, index, *args, **kwargs):
        self.app = app
        self.index = index
        self.process = process
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        message_dict['from'] = DEFAULT_FROM
        message_dict['index_name'] = self.index
        log_record['@timestamp'] = datetime.now().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['app'] = self.app
        log_record['process'] = self.process
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)


def setup_logging(app, log_path, process='main', index='default_index', log_level='INFO'):
    json_handler = logging.StreamHandler()
    handlers = [
        logging.StreamHandler()
    ]

    if os.getenv('ENVIRONMENT') == 'production':
        formatter = ElkJsonFormatter(
            app=app,
            process=process,
            index=index,
            fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        json_handler.setFormatter(formatter)

        file_handler = TimedRotatingFileHandler(log_path, backupCount=2)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(json_handler)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )

    def my_handler(type, value, tb):
        logging.exception("Uncaught exception: {0}".format(str(value)))

    sys.excepthook = my_handler
