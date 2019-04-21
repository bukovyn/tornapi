#!/usr/bin/env python3

import json
import os.path
import pymysql.cursors
import tornado.httpserver
import tornado.ioloop
import tornado.web
from config import Config


class Application(tornado.web.Application):
	""" Tornado and database setup.
	"""

	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
			(r"/{table}".format(
				table=Config.DATABASE['TABLE']), DatabaseHandler),
			(r"/{table}/([0-9]+)".format(
				table=Config.DATABASE['TABLE']), TableHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True
		)
		super(Application, self).__init__(handlers, **settings)

		# initial database connection
		self.db = pymysql.connect(
			host=Config.DATABASE['HOST'],
			user=Config.DATABASE['USER'],
			password=Config.DATABASE['PASSWORD'],
			db=Config.DATABASE['SCHEMA'],
			charset=Config.DATABASE['CHARSET'],
			cursorclass=pymysql.cursors.DictCursor
		)


class BaseHandler(tornado.web.RequestHandler):
	""" Default handler.
	"""

	@property
	def db(self):
		""" Get database instance.
		"""
		return self.application.db

	@property
	def json_data(self):
		""" Get request body in JSON.
		"""
		try:
			return tornado.escape.json_decode(self.request.body)
		except:
			return {}

	def execute(self, query):
		""" Executes a query on the database.

		Args:
			query (str): The query being executed.
		Returns:
			The result of the query.
		Raises:
			HTTPError: A 404 if item does not exist in the database.
		"""
		db = self.db
		cursor = db.cursor()
		cursor.execute(query)
		result = cursor.fetchall()
		db.commit()

		if result:
			data = json.dumps(result)
			return data
		# if id does not exist in database
		elif self.request.method == 'GET' and all(result):
			raise tornado.web.HTTPError(404)
		else:
			return result

	def update_row(self, body, item_id):
		""" Updates existing row(s) in the database.

		Args:
			body (dict): Item(s)
			item_id (int): Item ID.
		"""
		# Compose query
		values = ""
		for entry in body:
			values += "`{}`='{}', ".format(entry, body[entry])
		values = values[:-2]

		query = """
			UPDATE {}
			SET {}
			WHERE id={}
		""".format(Config.DATABASE['TABLE'], values, item_id)
		self.execute(query)

	def insert_row(self, body):
		""" Inserts new row(s) into the database.

		Args:
			body (dict): The data being inserted.
		"""
		columns, values = [], []
		for entry in body:
			columns.append(entry)
			values.append(body[entry])

		columns = "({})".format(', '.join(columns))
		data = {
			'columns': columns,
			'values': tuple(values)
		}

		query = """
			INSERT INTO {} {}
			VALUES {}
		""".format(Config.DATABASE['TABLE'], data['columns'], data['values'])
		self.execute(query)

	def exists(self, item_id):
		""" Checks database if item exists.

		Args:
			item_id (int): Item ID.
		Returns:
			(bool)
		"""
		query = """
			SELECT *
			FROM {}
			WHERE id={}
		""".format(Config.DATABASE['TABLE'], item_id)
		result = self.execute(query)

		return False if isinstance(result, tuple) else True


class IndexHandler(BaseHandler):
	""" Handles routes to the default endpoint
	"""

	def get(self):
		""" Renders a homepage with instructions on how the API works.
		"""
		self.render("index.html")


class DatabaseHandler(BaseHandler):
	""" Handles routes to '/table'
		Responsible for all the database manipulation.
	"""

	def get(self):
		""" Displays the table in the form of a JSON object.
		"""
		query = "SELECT * from {table}".format(table=Config.DATABASE['TABLE'])
		self.render("result.html", data=self.execute(query))

	def post(self):
		""" Inserts entries into the database.
			Insertions are specific to the contents of the request.
		"""
		data = self.json_data
		if data:
			for entry in data:
				result = self.insert_row(data[entry])

	def put(self):
		""" Updates database entries.
			Updates are specific to the contents of the request.
		"""
		data = self.json_data
		if data:
			for entry in data:
				if self.exists(entry):
					result = self.update_row(data[entry], entry)

	def delete(self):
		"""Deletes entries from the database.
		Deletions are specific to the contents of the request.
		"""
		data = self.json_data
		if data:
			for entry in data:
				if self.exists(entry):
					query = """
						DELETE
						FROM {}
						WHERE id={}
					""".format(Config.DATABASE['TABLE'], entry)
					result = self.execute(query)


class TableHandler(BaseHandler):
	""" Handles routes to '/table/[0-9]+'
		Uses regular expressions to handle numbers.
		Displays table information based on id specified.
	"""

	def get(self, item_id):
		""" Displays table information in the form of a JSON object.

		Args:
			id (int): Item ID.
		"""
		query = """
			SELECT *
			FROM {}
			WHERE id={}
		""".format(Config.DATABASE['TABLE'], item_id)
		self.render("result.html", data=self.execute(query))


def main():
	""" Initiates the application.
	"""
	http_server = tornado.httpserver.HTTPServer(Application())
	# by default accessible at localhost port 8000 '127.0.0.1:8000'
	http_server.listen(8000)
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()
