from jobs import sql

def insert_default_settings():
	
	search_admin = sql.session.query(sql.Role_user).filter_by(name='admin').first()
	if search_admin is None:
		adm = sql.Role_user(name='admin',admin=True)
		sql.session.add(adm)
		sql.session.commit()
		
		id_admin = adm.id
	else:
		id_admin = search_admin.id

			
	search_user = sql.session.query(sql.Role_user).filter_by(name='user').first()
	if search_user is None:
		user = sql.Role_user(name='user',admin=False)
		sql.session.add(user)
		sql.session.commit()

	result_search = sql.session.query(sql.User).filter_by(username='admin').first()
	if result_search is None:

		user_admin = sql.User(username='admin',
						password_hash='pbkdf2:sha256:150000$F0Q7mKci$c416f09ac48c58f093598e196f9c76918fe04e7a1cc9a27b92ffafcf1c4d855b',
						comment='',
						role = id_admin)
		
		sql.session.add(user_admin)
		sql.session.commit()

	result_search = sql.session.query(sql.User).filter_by(username='External_user').first()
	if result_search is None:
		
		user_external = sql.User(username='External_user',
						password_hash='pbkdf2:sha256:150000$MXzxabqn$d3dda60fced3ce1c7017c7d28cb68b876df07e087dc0fe1d77fefcb99a9bc5ea',
						comment='',
						role = id_admin)
		
		sql.session.add(user_external)
		sql.session.commit()	
