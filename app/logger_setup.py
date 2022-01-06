"""
logger_setup.py customizes the apps logging module.Each time an event is logged the
logger checks the level of the event (eg. debug, warning, info....). If the event is
above the approved threshold then it goes through. The handlers do the same thing;
they output to a file/shell if the event is above their threshold.

Example:
    >>> from website import logger
    >>> loggger.info('event', foo='bar')

**Levels**:
    - logger.debug('For debugging purposes')
    - logger.info('an event occureed, for example a database update')
    - logger.warning('Rare situation')
    - logger.error('Something went wong')
    - logger.critical('Very very bad')

you can build a log incrementally as so:
    >>> log = logger.new(date='now')
    >>> log = log.bind(weather ='rainy')
    >>> log.info('user logged in', user='john')
    
"""

import datetime as dt
import logging
from logging.handlers import RotatingFileHandler
import pytz

from  flask import request, session
from structlog import wrap_logger
from structlog.processors import JSONRenderer

from app import app

#set the logging level
app.logger.removeHandler(app.logger.handlers[0])
TZ = pytz.timezone(app.config['TIMEZONE'])

def add_fields(_, level, event_dict):
    """ add custom fields to each record."""
    now = dt.datetime.now()
    event_dict['timestamp'] = TZ.localize(now, True).astimezone(pytz.utc)
    event_dict['level'] = level


    if session:
        event_dict['session_id'] = session.get('session.id')
    if request:
        try:
            event_dict['ip_address'] = request.headers['X-Forwarded-For'].split(',')[0].strip()
        except:
            event_dict['ip_address'] = 'unknown'
    return event_dict


#add a handler to write log messages to a file
if app.config.get('LOG_FILENAME'):
    file_handler = RotatingFileHandler(
        filename= app.config['LOG_FILENAME'],
        maxBytes = app.config['LOG_MAXBYTES'],
        mode = 'a',
        encoding = 'utf-8'
        )
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)


#wrap the application logger with structog to format the output
logger = wrap_logger(
    app.logger,
    processors=[
        add_fields,
        JSONRenderer(indent=None)]
    )
