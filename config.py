class Config:
	""" Database configuration variables.
			Set to the default values for MySQL databases hosted locally.
	"""
	DATABASE = {
		'HOST': '127.0.0.1',
		'USER': 'root',
		'PASSWORD': '',
		'SCHEMA': 'university',
		'TABLE': 'students',
		'CHARSET': 'utf8'
	}
