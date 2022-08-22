#!/usr/bin/python3

import MySQLdb

class DB:

	def __init__(self, dbuser, dbpass, dbname):
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbname = dbname

	def connect(self):
		self.db = MySQLdb.connect('localhost', self.dbuser, self.dbpass, self.dbname)

	def insert(self, records):
		c=self.db.cursor()
		query = """INSERT INTO odczyty (flatno, co_count, cw_count, hw_count) VALUES (%s, %s, %s, %s)"""
		print(query)
		for record in records:
			print(record)
			val = (record['flatno'], record['co_count'], record['cw_count'], record['hw_count'])
			print(val)
			c.execute(query, val)
		self.db.commit()

	def get_day(self, day):
		pass

	def close(self):
		self.db.close()


if __name__ == '__main__':
	db = DB('mbus', 'mbus', 'bukowa')
	db.connect()
	record = {'co_count' : 1, 'cw_count' : 2, 'hw_count' : 3, 'flatno' : 1}
	db.insert(record)
	db.close()

