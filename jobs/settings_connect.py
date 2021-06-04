import os

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