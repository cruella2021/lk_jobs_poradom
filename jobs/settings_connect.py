import os
'''Загрузка переменных'''
class Config():
	
	def __init__(self):
		#1C login and pass
		self.IP_HOST_1C 	= os.getenv('IP_HOST_1C')
		self.LOGIN_1C 		= os.getenv('LOGIN_1C')
		self.PASSWORD_1C 	= os.getenv('PASSWORD_1C')

		#External DB 
		self.IP_HOST_DB 	= os.getenv('IP_HOST_DB')
		self.IP_HOST_DB 	= os.getenv('IP_HOST_DB')
		self.PASSWORD_DB 	= os.getenv('PASSWORD_DB')
		self.NAME_DB 		= os.getenv('Name_DB')
		self.ERROR          = False       
		self.ERROR_TEXT 	= ''

		if self.IP_HOST_1C is None:
			self.ERROR = True
			self.ERROR_TEXT = 'Set param IP_HOST_1C\n'

		if self.LOGIN_1C is None:
			self.ERROR = True
			self.ERROR_TEXT = self.ERROR_TEXT + 'Set param LOGIN_1C\n'

		if self.PASSWORD_1C is None:
			self.ERROR = True
			self.ERROR_TEXT = self.ERROR_TEXT + 'Set param PASSWORD_1C\n'

		if self.IP_HOST_DB is None:
			self.ERROR = True
			self.ERROR_TEXT = self.ERROR_TEXT + 'Set param IP_HOST_DB\n'

		if self.PASSWORD_DB is None:
			self.ERROR = True
			self.ERROR_TEXT = self.ERROR_TEXT + 'Set param PASSWORD_DB\n'

		if self.NAME_DB is None:
			self.ERROR = True
			self.ERROR_TEXT = self.ERROR_TEXT + 'Set param NAME_DB\n'
