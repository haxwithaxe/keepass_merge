#!/usr/bin/env python3

# requires: keepassdb

import json
import logging

from keepassdb import Database


DEFAULT_LOG_LEVEL = logging.INFO


def make_new_entry_spec(entry):
	entry_dict = entry.to_dict()
	for key in ['modified', 'uuid', 'group_id', 'created']:
		del entry_dict[key]
	return entry_dict


class DB:

	def __init__(self, db_filename, passwd):
		self.logger = logging.getLogger('keepass_merge')
		self.db = Database(db_filename, passwd)
		self.backup = self.db.groups[-1]
		self.uuids = [x.uuid for x in self.db.entries]
		self.groups = [x.id for x in self.db.groups]

	def get_group(self, group_id):
		return [x for x in self.db.groups if x.id == group_id][0]

	def get_entry(self, uuid):
		return [x for x in self.db.entries if x.uuid == uuid][0]

	def merge_entry(self, other):
		""" Assumes the same title and group. """
		self_entry = self.get_entry(other.uuid)
		if self_entry.modified < other.modified:
			self.logger.debug('update %s', other.title)
			other_spec = make_new_entry_spec(other)
			self.db.create_entry(self_entry.group, **other_spec)
			self.db.move_entry(self_entry, self.backup)
		elif self_entry.modified == other.modified:
			self.logger.debug('same %s', other.title)
		else:
			self.logger.debug('just backup %s', other.title)
			copy_spec = make_new_entry_spec(other)
			self.db.create_entry(self.backup, **copy_spec)

	def update(self, other):
		for entry in other.db.entries:
			if entry.uuid not in self.uuids:
				if entry.group_id == self.backup.id:
					continue
				if entry.group_id in self.groups:
					group = self.get_group(entry.group_id)
				else:
					self.logger.debug('make group %s', entry.group.title)
					group = self.db.create_group(title=entry.group.title, icon=entry.group.icon)
				self.db.create_entry(group, **make_new_entry_spec(entry))
			else:
				self.merge_entry(entry)

	def __getattr__(self, attr):
		return getattr(self.db, attr)


def load_config(filename):
	with open(filename, 'r') as config_file:
		config = json.load(config_file)
	return config


def merge_databases(args):
	logger = logging.getLogger('keepass_merge')
	conf = load_config(args.config)
	master = conf.pop(0)
	db = DB(master['file'], master['password'])
	try:
		start_len = len(db.entries)
		for kdb in conf:
			cdb = DB(kdb['file'], kdb['password'])
			try:
				db.update(cdb)
			finally:
				cdb.close()
		db.save(password=master['password'])
		logger.debug('%s/%s', start_len, len(db.entries))
		logger.info('saved changes to %s', master['file'])
	except Exception as err:
		logger.error('failed to merge databases.', exc_info=True)
	finally:
		db.close()


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--config')
	parser.add_argument('-d', '--debug', required=False, const=True, action='store_const')
	args = parser.parse_args()
	logging.basicConfig(level=logging.WARN)
	logging.getLogger('keepass_merge').setLevel({True: logging.DEBUG, None: DEFAULT_LOG_LEVEL}[args.debug])
	merge_databases(args)
