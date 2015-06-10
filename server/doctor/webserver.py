import sys
import base64
import uuid
import json
import argparse
import configparser
import logging
import logging.config

import tornado.ioloop
import tornado.web

from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker

from .handlers import doctor_registration_api as doctor_registration_handlers

def parse_config(config_file):
    config = configparser.RawConfigParser()
    config.read(config_file)
    return config

# class BaseRequestHandler(tornado.web.RequestHandler):
#   def get(self):
#       self.write("Hello, world")

# application = tornado.web.Application([
#   (r"/", BaseRequestHandler )
# ])

class WebApplication(tornado.web.Application):

    def __init__(self, config, main_loop=None):
        self.db = scoped_session(sessionmaker(bind=engine_from_config({
            'sqlalchemy.url': config.get('sqlalchemy', 'url'),
            'sqlalchemy.echo': config.getboolean('sqlalchemy', 'echo')
        })))
        logging.info('webapplication')
        settings = {
            'debug': True,
            'cookie_secret': str(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))
        }

        handlers = []
        handlers += doctor_registration_handlers
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    parser = argparse.ArgumentParser(description="Doc webapp init");
    parser.add_argument('--config', dest='config', required=True);
    args = parser.parse_args()
    if not args.config:
        parser.print_help()
        sys.exit(1)

    config = parse_config(args.config)
    if not config.has_option('docwebapp', 'port'):
        print('port is required')
        sys.exit(1);

    logging.config.fileConfig(args.config, disable_existing_loggers=0)
    logging.getLogger('tornado').setLevel(config.getint('docwebapp', 'logging'))
    logging.getLogger('webserver').info('<!> doc\'s webapp being initialized...')
    '''INIT SERVER'''
    main_loop = tornado.ioloop.IOLoop.instance()
    application = WebApplication(config=config, main_loop=main_loop)
    application.listen(config.getint('docwebapp', 'port'))
    logging.getLogger('webserver').info('<!> doc\'s webapp initialized (version = %s)' % ('0.0.1'))
    main_loop.start()

if __name__ == "__main__":
    main()