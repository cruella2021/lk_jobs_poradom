import mysql.connector
from datetime import date
import pysftp
from jobs import sql
import os

class Load_update_image():
	
	def __init__(self, default_settings):
		self.IP_HOST_DB		= default_settings.IP_HOST_DB
		self.USER_DB 		= default_settings.USER_DB
		self.PASSWORD_DB 	= default_settings.PASSWORD_DB
		self.NAME_DB 		= default_settings.NAME_DB
		self.IP_HOST_SSH	= default_settings.IP_HOST_SSH
		self.USER_SSH		= default_settings.USER_SSH
		self.PASSWORD_SSH	= default_settings.PASSWORD_SSH
		self.LOCAL_STORAGE_IAMGE= default_settings.LOCAL_STORAGE_IAMGE
		self.REMOTE_STORAGE_IAMGE= default_settings.REMOTE_STORAGE_IAMGE
	
	def delete_image(self):
		all_image = sql.session.query(sql.TableImage).all()
		for image_del in all_image:
			sql.session.delete(image_del)
		
		sql.session.commit()
		
	def load_images(self):

		list_object = sql.session.query(sql.TableObject).all()

		where_number = ','
		for object_id in list_object:
			where_number = where_number + '"'+ str(object_id.number) + '",'

		where_number = where_number[1:-1]

		mydb = mysql.connector.connect(host=self.IP_HOST_DB,user=self.USER_DB,password=self.PASSWORD_DB,database=self.NAME_DB) 
		mycursor = mydb.cursor() 
		query_image = """Select
			t_image.id,
			t_image.task_id,
			t_image.object_id, 
			t_image.date_updated,
			t_image.filename
			From images as t_image
			LEFT JOIN objects as t_objects
			ON t_image.object_id = t_objects.id
			Where t_objects.number in ({})""".format(where_number)
		
		mycursor.execute(query_image) 
		myresult =	mycursor.fetchall() 
		
		for str_cursor in myresult:
			id_image 	= str_cursor[0]
			id_task 	= str_cursor[1]
			id_object 	= str_cursor[2]
			date_update = str_cursor[3]
			filename 	= str_cursor[4]
		
			foundTask = sql.session.query(sql.TableStage).get(id_task) 
			if foundTask is None: 
				continue
			
			found_image = sql.session.query(sql.TableImage).get(id_image) 
			if found_image is None:
				newImage = sql.TableImage(id=id_image,
						id_object=foundTask.id_object,
						id_task=foundTask.id,
						date_updated=date_update,
						filename=filename) 

				sql.session.add(newImage)
			else: 
				found_image.d_object=foundTask.id_object 
				found_image.id_task=foundTask.id 
				found_image.date_updated=date_update 
				found_image.filename=filename
		
		sql.session.commit()

	def update_sum_image_in_stage(self):

		stageS = sql.session.query(sql.TableStage).all()
		for stage in stageS:
			sum_ = sql.session.query(sql.TableImage).filter(sql.TableImage.id_task==stage.id).count()
			if sum_ > 0:
				stage.number_image = sum_

		sql.session.commit()

	def upload_image_from_srv(self):

		str_srv = self.REMOTE_STORAGE_IAMGE#'/var/www/sporadom/httpdocs/web/uploads/'
		str_local = self.LOCAL_STORAGE_IAMGE#'/var/www/share/static/images/'

		rezult = sql.session.query(sql.TableImage).all()
		
		sftp = pysftp.Connection(host=self.IP_HOST_SSH,username=self.USER_SSH,password=self.PASSWORD_SSH)
		
		for row in rezult:
			srv = str_srv + row.filename
			local = str_local + row.filename
			if os.path.exists(local) == False:
				sftp.get(srv,local)
	
	def main(self):
		self.delete_image()
		self.load_images()
		self.update_sum_image_in_stage()
		self.upload_image_from_srv()
