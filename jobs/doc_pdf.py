import requests
import json
import base64
from jobs import sql
import os

def get_pdf_for_doc():

	rezult_table = sql.session.query(sql.TableObject).all()
	for doc in rezult_table:

		new_folder = '/var/www/share/static/pdf/{}/'.format(doc.number)
		if os.path.exists(new_folder) == False:
			os.mkdir(new_folder)
		else:
			# тут удаляю все файлы
			#нужно переделать!!!
			list_file = os.listdir(new_folder)
			for file in list_file:
				if os.path.isfile(new_folder + file):
					os.remove(new_folder + file)

		payload = json.dumps({'NumberDoc':doc.number,'DocType':'1'})
		
		r = requests.post('http://192.168.111.204/poradom_base/hs/GetTask/get_pdf',auth=("login","password"),data=payload)
		data = r.content

		try:
			dict_files = json.loads(data)
			for file_ in dict_files:
				
				if file_['pdf'] != None:
					new_file_name = '/var/www/share/static/pdf/{0}/{1}'.format(doc.number,file_['name'])
					file = open(new_file_name,'wb')
					file.write(base64.b64decode(file_['pdf']))
					file.close()
				else:
					print('Error')
		except:
			print('Error {}'.format(doc.number))

def get_pdf_for_dop():
	rezult_table = sql.session.query(sql.TableObject).all()
	for doc in rezult_table:
	
		new_folder = '/var/www/share/static/pdf/{}/dop/'.format(doc.number)
		if os.path.exists(new_folder) == False:
			os.mkdir(new_folder)
		else:
			# тут удаляю все файлы
			#нужно переделать!!!
			list_file = os.listdir(new_folder)
			for file in list_file:
				os.remove(new_folder + file)

		payload = json.dumps({'NumberDoc':doc.number,'DocType':'1'})
		
		r = requests.post('http://192.168.111.204/poradom_base/hs/GetTask/get_pdf_dop',auth=("login","password"),data=payload)
		data = r.content

		try:
			dict_files = json.loads(data)
			for file_ in dict_files:
				
				if file_['pdf'] != None:
					new_file_name = '/var/www/share/static/pdf/{0}/dop/{1}'.format(doc.number,file_['name'])
					file = open(new_file_name,'wb')
					file.write(base64.b64decode(file_['pdf']))
					file.close()
				else:
					print('Error')
		except:
			print('Error {}'.format(doc.number))
