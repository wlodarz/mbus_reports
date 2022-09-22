#!/usr/bin/python3

import MySQLdb

class DB:

	def __init__(self, dbuser, dbpass, dbname):
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbname = dbname

	def connect(self):
		self.db = MySQLdb.connect('localhost', self.dbuser, self.dbpass, self.dbname)

	def insert_odczyt(self, records):
		c=self.db.cursor()
		query = """INSERT INTO odczyty (mieszkanie, ogrzewanie, zimna, ciepla) VALUES (%s, %s, %s, %s)"""
		print(query)
		for record in records:
			print(record)
			val = (record['flatno'], record['co_count'], record['cw_count'], record['hw_count'])
			print(val)
			c.execute(query, val)
		self.db.commit()

	def update_alarms(self, alarms):
		c=self.db.cursor()
		query = """UPDATE alarmy SET ogrzewanie = %s, zimna = %s, ciepla = %s, time = NOW() WHERE mieszkanie = %s"""
		print(query)
		for alarm in alarms:
			print(alarms)
			val = (alarm['co_flag'], alarm['cw_flag'], alarm['hw_flag'], alarm['flatno'])
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
	db.insert_odczyt(record)
	alarms = [{'flatno' : 1, 'co_flag' : False, 'cw_flag' : False, 'hw_flag' : False}]
	db.insert_alarms(alarms)
	db.close()

