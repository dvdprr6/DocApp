import sys
import argparse
import configparser
import logging
import logging.config

import tornado.ioloop
import tornado.web

def parse_config(config_file):
	config = configparser.RawConfigParser()
	config.read(config_file)
	return config

class BaseRequestHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")

application = tornado.web.Application([
	(r"/", BaseRequestHandler )
])

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
	application.listen(config.getint('docwebapp', 'port'))
	logging.getLogger('webserver').info('<!> doc\'s webapp initialized (version = %s)' % ('0.0.1'))
	main_loop.start()

if __name__ == "__main__":
	main()