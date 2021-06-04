import mysql.connector
from datetime import date
import pysftp
from jobs import sql
import os

def delete_image():
	all_image = sql.session.query(sql.TableImage).all()
	for image_del in all_image:
		sql.session.delete(image_del)
	
	sql.session.commit()
	
def load_images():

	list_object = sql.session.query(sql.TableObject).all()

	where_number = ','
	for object_id in list_object:
		where_number = where_number + '"'+ str(object_id.number) + '",'

	where_number = where_number[1:-1]

	mydb = mysql.connector.connect(host="192.168.111.133",user="poradomdb_userr",password="ht6Bnc39Oirbv",database="poradomdbb") 
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

def update_sum_image_in_stage():

	stageS = sql.session.query(sql.TableStage).all()
	for stage in stageS:
		sum_ = sql.session.query(sql.TableImage).filter(sql.TableImage.id_task==stage.id).count()
		if sum_ > 0:
			stage.number_image = sum_

	sql.session.commit()

def upload_image_from_srv():

	host = '192.168.111.133'
	username = 'bisoft'
	password = 'jKbd9ejQ5xCm'
	str_srv = '/var/www/sporadom/httpdocs/web/uploads/'
	str_local = '/var/www/share/static/images/'

	rezult = sql.session.query(sql.TableImage).all()
	
	
	sftp = pysftp.Connection(host=host,username=username,password=password)
	
	for row in rezult:
		srv = str_srv + row.filename
		local = str_local + row.filename
		if os.path.exists(local) == False:
			sftp.get(srv,local)
