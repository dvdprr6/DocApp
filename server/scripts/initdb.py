import sys
import logging
import argparse
import configparser
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command

from doctor.db.models import Base

'''
To get the .db for sqlite
python scripts/initdb.py --config=conf/test/docs.conf
'''

def parse_config(config_file):
	config = configparser.RawConfigParser()
	config.read(config_file)
	return config

def initialize_database(config, args):
	db_url = config.get('sqlalchemy', 'url')
	db_echo = config.getboolean('sqlalchemy', 'echo')
	DbEngine = create_engine(db_url, echo=db_echo)
	stamp_alembic_version(args)
	Base.metadata.create_all(DbEngine)

def stamp_alembic_version(args):
	alembic_cfg = Config(args.config)
	command.stamp(alembic_cfg, 'head')

def main(argv=sys.argv):
	parser = argparse.ArgumentParser(description='Doctor DB Init')
	parser.add_argument('--config', dest='config', required=True)
	args = parser.parse_args()
	if not args.config:
		parser.print_help()
		sys.exit(1)
	config = parse_config(args.config)
	initialize_database(config, args)

if __name__ == '__main__':
	main()