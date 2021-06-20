from sqlalchemy import Column, Integer, String, create_engine, Boolean, ForeignKey, DateTime
import sqlalchemy.orm as create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

fl_debug_sql = False
engine = create_engine('sqlite:///db.db',echo=fl_debug_sql)

Base = declarative_base()

class Available_stage(Base):
	__tablename__ = 'available_stage'

	id = Column(Integer, primary_key=True)
	name = Column(String(150))
	description = Column(String(150))

class Role_user(Base):
	__tablename__ = 'role_user'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	admin	= Column(Boolean)

	def __repr__(self):
		return '{}'.format(self.name)

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	username = Column(String(64), index=True, unique=True)
	password_hash = Column(String(128))
	comment = Column(String(140))
	role = Column(Integer,ForeignKey('role_user.id'),nullable=False)

class TableObject(Base):
	__tablename__ = 'table_object'

	id = Column(Integer, primary_key=True)
	number 	= Column(String(9), index=True, unique=True)
	fio 	= Column(String(255), index=True, unique=False)
	email	= Column(String(255), index=True, unique=False)
	tel	= Column(String(255), index=True, unique=False)
	address	= Column(String(255), index=True, unique=False)
	project	= Column(String(255), index=True, unique=False)
	date_doc = Column(DateTime,default=date(1,1,1))
	date_reliz = Column(DateTime,default=date(1,1,1))

class TableStage(Base):
	__tablename__ = 'table_stage'

	id 			= Column(Integer, primary_key=True)
	title 			= Column(String(255), index=True, unique=False)
	id_object		= Column(Integer,ForeignKey('table_object.id'),nullable=False)
	planned_start_date	= Column(DateTime,default=date(1,1,1))
	planned_end_date	= Column(DateTime,default=date(1,1,1))
	real_start_date		= Column(DateTime,default=date(1,1,1))
	real_end_date		= Column(DateTime,default=date(1,1,1))
	number_image		= Column(Integer)

class TableImage(Base):
	__tablename__ = 'table_image'

	id = Column(Integer, primary_key=True)
	id_object = Column(Integer,ForeignKey('table_object.id'),nullable=False)
	id_task = Column(Integer,ForeignKey('table_stage.id'),nullable=False)
	date_updated = Column(DateTime,default=date(1,1,1))
	filename = Column(String(255), index=True, unique=False)

class TablePartner(Base):
	__tablename__ = 'table_partner'

	id 			= Column(Integer, primary_key=True)
	type_user 	= Column(String(255), unique=False)
	fio 		= Column(String(255), unique=False)
	telephone 	= Column(String(255),unique=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
