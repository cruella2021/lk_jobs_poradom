# -*- coding: utf-8 -*-

from jobs import sql
import mysql.connector
import json
import requests
from datetime import date,datetime

class Doc_and_stage():
    
    def __init__(self, default_settings):
        self.IP_HOST_1C     = default_settings.IP_HOST_1C
        self.LOGIN_1C       = default_settings.LOGIN_1C
        self.PASSWORD_1C    = default_settings.PASSWORD_1C
        self.IP_HOST_DB     = default_settings.IP_HOST_DB
        self.USER_DB        = default_settings.USER_DB
        self.PASSWORD_DB    = default_settings.PASSWORD_DB
        self.NAME_DB        = default_settings.NAME_DB
        
    def delet_all_doc(self):
        result_search = sql.session.query(sql.TableObject).all()
        for doc in result_search:
            sql.session.delete(doc)

        sql.session.commit()
        
    def cleaning_unused_objects(self):

        r = requests.post('http://'+ self.IP_HOST_1C +'/poradom_base/hs/GetTask/get_list_number_doc',auth=(self.LOGIN_1C,self.PASSWORD_1C)) 
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

                '''Удалим все этапы этого документа, удаляем картинки и партнеров'''

                del_partner = sql.session.query(sql.TablePartner).filter_by(id=doc.id).all()
                for partner in del_partner:
                    sql.session.delete(partner)
                    
                
                del_stage = sql.session.query(sql.TableStage).filter_by(id_object=doc.id).all()
                for stage in del_stage:
                    sql.session.delete(stage)
             
                    del_images = sql.session.query(sql.TableImage).filter_by(id_task=stage.id).all()
                    for image in del_images:
                        sql.session.delete(image)
                '''После удаления подчиненых записей удалим основной документ'''
                sql.session.delete(doc)
                
            sql.session.commit()
            
            
    def delete_all_stage(self):
        all_stage = sql.session.query(sql.TableStage).all()
        for stage_del in all_stage:
            sql.session.delete(stage_del)
            
        sql.session.commit()
            
    def load_object(self):

        r = requests.post('http://' + self.IP_HOST_1C + '/poradom_base/hs/GetTask/get_list_number_doc',auth=(self.LOGIN_1C,self.PASSWORD_1C)) 
        Data = r.content 
        if Data:
            list_docs = json.loads(Data)

        where_number = ','
        for doc_number in list_docs:
            where_number = where_number + '"'+ doc_number + '",'

        where_number = where_number[1:-1]

        mydb = mysql.connector.connect(host=self.IP_HOST_DB,user=self.USER_DB,password=self.PASSWORD_DB,database=self.NAME_DB) 

        mycursor = mydb.cursor()
        query_object = """Select
            t_objects.id,
            t_objects.number,
            t_objects.fio
        
        From objects_1c as t_objects
        where t_objects.number in ({})
        """.format(where_number)


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

            result_search = sql.session.query(sql.TableObject).filter_by(number=clm_number).first()


            if result_search is None: 
                #newObject = sql.TableObject(number=clm_number,fio=clm_fio)
                #sql.session.add(newObject)
                print("DOC not FOUND {}".format(clm_number))
            else: 
                result_search.number    = clm_number 
                result_search.fio       = clm_fio
                
                sql.session.commit()
                
            #sql.session.commit()

    def load_available_stage(self):

        r = requests.post('http://' + self.IP_HOST_1C + '/poradom_base/hs/GetTask/get_stages',auth=(self.LOGIN_1C,self.PASSWORD_1C)) 
        Data = r.content 
        if Data:
            list_stages = json.loads(Data)
        
        '''Удалим все этапы доступные этапы'''
        all_avaliable_stage = sql.session.query(sql.Available_stage).all()
        for avaliable_stage in all_avaliable_stage:
            sql.session.delete(avaliable_stage)
        
        
        '''Создадим доступные этапы'''
        for l_stag in list_stages:
                newStage = sql.Available_stage(name=l_stag['Stage'],description=l_stag['Description'])
                sql.session.add(newStage)
            
        sql.session.commit()

    def load_email_tel(self): 
        '''ТУТ переделать так как очень долго!!!'''
        select_row = sql.session.query(sql.TableObject).all()
        for row in select_row:
            payload = json.dumps({'Number':row.number}) 

            r = requests.post('http://' + self.IP_HOST_1C +'/poradom_base/hs/GetTask/info_object',auth=(self.LOGIN_1C,self.PASSWORD_1C),data=payload) 
            Data = r.content 
            if Data:
                dic = json.loads(Data)
        
                row.email   = dic['ЭлектронныйАдрес'] 
                row.tel     = dic['Телефон']
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
            
        sql.session.commit()

    def load_stage(self):

        stages = sql.session.query(sql.Available_stage).all()


        where_number = ','
        for stage in stages:
            where_number = where_number + '"'+ stage.name + '",'

        where_number = where_number[1:-1]

        mydb = mysql.connector.connect(host=self.IP_HOST_DB,user=self.USER_DB,password=self.PASSWORD_DB,database=self.NAME_DB) 
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

            clm_object_number       = str_cursor[0] 
            clm_id                  = str_cursor[1] 
            clm_title               = str_cursor[2] 
            clm_planned_start_date  = date(1,1,1) if str_cursor[3] is None else str_cursor[3] 
            clm_planned_end_date    = date(1,1,1) if str_cursor[4] is None else str_cursor[4]
            clm_real_start_date     = date(1,1,1) if str_cursor[5] is None else str_cursor[5] 
            clm_real_end_date       = date(1,1,1) if str_cursor[6] is None else str_cursor[6]

            if clm_object_number is None: 
                continue 

            resultObject = sql.session.query(sql.TableObject).filter_by(number=clm_object_number).first()
            if resultObject is None:
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
                resultStage.title               = clm_title 
                resultStage.id_object           = resultObject.id 
                resultStage.planned_start_date  = clm_planned_start_date 
                resultStage.planned_end_date    = clm_planned_end_date 
                resultStage.real_start_date     = clm_real_start_date 
                resultStage.real_end_date       = clm_real_end_date

        sql.session.commit()

    def rename_stage(self):
        '''Переименуем название этапов для отораения'''
        stages = sql.session.query(sql.Available_stage).all()

        for stage in stages:
            all_rename = sql.session.query(sql.TableStage).filter_by(title=stage.name).all()
            for one in all_rename:
                if one.title != stage.description:
                    one.title = stage.description
        sql.session.commit()

    def load_partners(self):

        r = requests.post('http://' + self.IP_HOST_1C + '/poradom_base/hs/GetTask/get_partners',auth=(self.LOGIN_1C,self.PASSWORD_1C)) 
        Data = r.content 
        if Data:
            list_partner = json.loads(Data)

            for partner in list_partner:
                fio         = partner['fio']
                telephone   = partner['telephone']

                partner_find = sql.session.query(sql.TablePartner).filter_by(fio=fio).first()
                if partner_find:
                    partner_find.type_user = 'partner'
                    partner_find.fio        = fio
                    partner_find.telephone  = telephone

                else:
                    new_partner = sql.TablePartner(type_user = 'partner',
                                        fio = fio,
                                        telephone = telephone)
                    sql.session.add(new_partner)

        sql.session.commit()

    def main(self):
        ##self.delete_all_stage()
        self.cleaning_unused_objects()
        self.load_object()
        self.load_available_stage()
        self.load_email_tel()
        self.load_stage()
        self.rename_stage()
        self.load_partners()
