from jobs import sql
import mysql.connector
import json
import requests
from datetime import date,datetime

def delet_all_doc():
	result_search = sql.session.query(sql.TableObject).all()
	for doc in result_search:
		sql.session.delete(doc)

	sql.session.commit()
	
def remote_delete_objects():

	r = requests.post('http://192.168.111.204/poradom_base/hs/GetTask/get_list_number_doc',auth=("web","passwd0")) 
	Data = r.content 
	if Data:
		list_docs = json.loads(Data)

	result_search = sql.session.query(sql.TableObject).all()
	for doc in result_search:
		fl = False
		
		for avaliavle_doc in list_docs:
			if doc.number == avaliavle_doc.strip():
				fl = True
		
		if fl == False:
			sql.session.delete(doc)
			
			del_stage = sql.session.query(sql.TableStage).filter_by(id_object=doc.number).all()
			for stage in del_stage:
				sql.session.delete(stage)
				
	sql.session.commit()
	
def delete_all_stage():
	all_stage = sql.session.query(sql.TableStage).all()
	for stage_del in all_stage:
		sql.session.delete(stage_del)
		
	sql.session.commit()
		
def load_object():

	r = requests.post('http://192.168.111.204/poradom_base/hs/GetTask/get_list_number_doc',auth=("web","passwd0")) 
	Data = r.content 
	if Data:
		list_docs = json.loads(Data)

	where_number = ','
	for doc_number in list_docs:
		where_number = where_number + '"'+ doc_number + '",'

	where_number = where_number[1:-1]

	mydb = mysql.connector.connect(host="192.168.111.133",user="poradomdb_userr",password="ht6Bnc39Oirbv",database="poradomdbb") 

	mycursor = mydb.cursor()
	query_object = """Select
		t_objects.id,
		t_objects.number,
		t_objects.fio
	
	From objects_1c as t_objects
	where t_objects.number in ({})
	""".format(where_number)

	#From objects_1c as t_objects

	mycursor.execute(query_object) 
	myresult = mycursor.fetchall() 
	
	for str_cursor in myresult:
		clm_id = str_cursor[0]
		clm_number = str_cursor[1]
		clm_fio = str_cursor[2]


		if clm_number is None or len(clm_number) < 1: 
			continue
		if clm_fio is None or len(clm_fio) < 1:
			continue 

		#result_search = sql.session.query(sql.TableObject).filter_by(id=clm_id).first()
		result_search = sql.session.query(sql.TableObject).filter_by(number=clm_number).first()


		if result_search is None: 
			#newObject = sql.TableObject(id=clm_id,number=clm_number,fio=clm_fio)
			newObject = sql.TableObject(number=clm_number,fio=clm_fio)
			sql.session.add(newObject)
		else: 
			#result_search.id		= clm_id
			result_search.number 	= clm_number 
			result_search.fio 		= clm_fio

		sql.session.commit()

def load_available_stage():

	r = requests.post('http://192.168.111.204/poradom_base/hs/GetTask/get_stages',auth=("web","passwd0")) 
	Data = r.content 
	if Data:
		list_stages = json.loads(Data)
	
	for l_stag in list_stages:

		found_stage = sql.session.query(sql.Available_stage).filter_by(name=l_stag['Stage']).first()

		if found_stage is None: 
			newStage = sql.Available_stage(name=l_stag['Stage'],description=l_stag['Description'])
			sql.session.add(newStage)
		else:
			sql.session.delete(found_stage)
			#found_stage.description = l_stag['Description']
			newStage = sql.Available_stage(name=l_stag['Stage'],description=l_stag['Description'])
			sql.session.add(newStage)

	sql.session.commit()

def load_email_tel(): 
	
	select_row = sql.session.query(sql.TableObject).all()
	for row in select_row:
		payload = json.dumps({'Number':row.number}) 

		r = requests.post('http://192.168.111.204/poradom_base/hs/GetTask/info_object',auth=("web","passwd0"),data=payload) 
		Data = r.content 
		if Data:
			dic = json.loads(Data)
	
			row.email 	= dic['ЭлектронныйАдрес'] 
			row.tel 	= dic['Телефон']
			row.address = dic['Адрес']
			row.project = dic['Проект']
			
			row.date_reliz = datetime.strptime(dic['ФактическаяДатаСдачиДома'],'%Y%m%d%H%M%S')
			
			row.date_doc = datetime.strptime(dic['ДатаДокумента'],'%Y%m%d%H%M%S')
			
			if row.email is None: 
				row.email = ''
		
			if row.tel is None: 
				row.tel = ''

			if row.address is None: 
				row.address = ''

			#if row.project is None: 
			#	row.project = ''
		
	sql.session.commit()

def load_stage():

	stages = sql.session.query(sql.Available_stage).all()


	where_number = ','
	for stage in stages:
		where_number = where_number + '"'+ stage.name + '",'

	where_number = where_number[1:-1]

	mydb = mysql.connector.connect(host="192.168.111.133",user="poradomdb_userr",password="ht6Bnc39Oirbv",database="poradomdbb") 
	mycursor = mydb.cursor()

	'''query_stage = """Select
		t_task.object_id,
		t_task.id,
		t_task.title, 
		t_task.planned_start_date,
		t_task.planned_end_date, 
		t_task.real_start_date,
		t_task.real_end_date
	From task as t_task
	where t_task.title in ({})
	""".format(where_number)'''

	query_stage = """Select
		t_objects.number,
		t_task.id,
		t_task.title, 
		t_task.planned_start_date,
		t_task.planned_end_date, 
		t_task.real_start_date,
		t_task.real_end_date
	From task as t_task
	Left Join objects as t_objects
	On t_task.object_id = t_objects.id
	where t_task.title in ({})
	""".format(where_number)

	
	
	mycursor.execute(query_stage) 
	myresult = mycursor.fetchall() 
	for str_cursor in myresult:

		clm_object_number 		= str_cursor[0] 
		clm_id 					= str_cursor[1] 
		clm_title 				= str_cursor[2] 
		clm_planned_start_date 	= date(1,1,1) if str_cursor[3] is None else str_cursor[3] 
		clm_planned_end_date 	= date(1,1,1) if str_cursor[4] is None else str_cursor[4]
		clm_real_start_date 	= date(1,1,1) if str_cursor[5] is None else str_cursor[5] 
		clm_real_end_date 		= date(1,1,1) if str_cursor[6] is None else str_cursor[6]

		if clm_object_number is None: 
			continue 

		resultObject = sql.session.query(sql.TableObject).filter_by(number=clm_object_number).first()
		#resultObject = sql.session.query(sql.TableObject).get(clm_object_number) 
		if resultObject is None:
			#if clm_object_id == '330':
			#	print(clm_object_id)
			continue

		resultStage = sql.session.query(sql.TableStage).get(clm_id) 
		if resultStage is None:
			newStage = sql.TableStage(id=clm_id,
					title=clm_title,
					id_object=resultObject.id,
					planned_start_date=clm_planned_start_date,
					planned_end_date=clm_planned_end_date, 
					real_start_date=clm_real_start_date,
					real_end_date=clm_real_end_date)
			
			sql.session.add(newStage) 
		else: 
			resultStage.title 				= clm_title 
			resultStage.id_object 			= resultObject.id 
			resultStage.planned_start_date 	= clm_planned_start_date 
			resultStage.planned_end_date 	= clm_planned_end_date 
			resultStage.real_start_date 	= clm_real_start_date 
			resultStage.real_end_date 		= clm_real_end_date

	sql.session.commit()

def rename_stage():
	stages = sql.session.query(sql.Available_stage).all()

	for stage in stages:
		all_rename = sql.session.query(sql.TableStage).filter_by(title=stage.name).all()
		for one in all_rename:
			one.title = stage.description
	sql.session.commit()

def load_partners():

	r = requests.post('http://192.168.111.204/poradom_base/hs/GetTask/get_partners',auth=("web","passwd0")) 
	Data = r.content 
	if Data:
		list_partner = json.loads(Data)

		for partner in list_partner:
			fio 		= partner['fio']
			telephone 	= partner['telephone']

			partner_find = sql.session.query(sql.TablePartner).filter_by(fio=fio).first()
			if partner_find:
				partner_find.type_user = 'partner'
				partner_find.fio 		= fio
				partner_find.telephone	= telephone

			else:
				new_partner = sql.TablePartner(type_user = 'partner',
									fio = fio,
									telephone = telephone)
				sql.session.add(new_partner)

	sql.session.commit()