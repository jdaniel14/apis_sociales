
"""
	### REQUESTS DE POSTS DE USUARIO
"""
"""
user = api.user_search(q = "MUNDOLIGHT", count = 1)

id = user[0][0].id
full_name = user[0][0].full_name
"""

"""
datos = api.user_recent_media(user_id = id, max_id = "791327843216117314_1034466" )

i = 0

posts = ""
json_posts = ""
next_link = ""

for item in datos:
	
	tipo =  str(type(item))
	print tipo
	
	if ("list" in tipo):
		posts = item
		
	if("str" in tipo):
		json_posts = item 	

	if("unicode" in tipo):
		next_link = item

print next_link

#print json_posts

inicio = next_link.find("max_id=")
inicio = inicio + 7
max_id = next_link[inicio:]



print max_id


for item in posts:
	print str(i) + ") " + str(item)
	print item.id

	if(hasattr(item.caption,'text')):
		print item.caption.text
	
	print item.link
	print
	i = i + 1

"""

"""
for item in api.media_popular():
	print str(i) + ") " + str(item.caption)
	print
	i = i + 1

"""

"""
datos = api.media_search(lat = -12.047, lng = -77.062)

for item in datos:
	print item.caption
	print

"""



"""
##### REQUESTS DE tags


# 5000 requests por hora (o 20)

datos = api.tag_recent_media(tag_name = "peru", max_tag_id = 1410999555064759)

#print type(datos)

posts = ""
json_posts = ""
next_link = ""

for item in datos:
	
	tipo =  str(type(item))
	print tipo
	
	if ("list" in tipo):
		posts = item
		
	if("str" in tipo):
		json_posts = item 	

	if("unicode" in tipo):
		next_link = item

print next_link

print

#print json_posts

print


for item in posts:
	print str(i) + ") " + str(item)
	print item.id

	if(hasattr(item.caption,'text')):
		print item.caption.text
	
	print item.link
	print
	i = i + 1



#print datos[0]

"""








"""

	i = 0

	tag_name = "peru"

	posts = ""
	json_posts = ""
	next_link = ""
	lista_jsons = ""
	cargado_post = False

	datos = api.tag_recent_media(tag_name = tag_name)
	id_ant = ""

	while (True):

		cargado_post = False
		lista_jsons = ""
		for item in datos:
			
			tipo =  str(type(item))
			print tipo
			
			if (("list" in tipo) and (not(cargado_post))):
				posts = item
				cargado_post = True
			elif ("str" in tipo):
				json_posts = item
			elif ("unicode" in tipo):
				next_link = item
			elif(("list" in tipo) and (cargado_post)):
				lista_jsons = item

		inicio = next_link.find("max_tag_id=")
		inicio = inicio + 11
		max_tag_id = next_link[inicio:]

		j = 0
		for item in posts:
			print str(i) + ") " + str(item)
			print item.id

			if(hasattr(item.caption,'text')):
				print item.caption.text
			
			print item.link
			print lista_jsons[j]
			print
			linea =  to_CSV(item)
			print linea
			print
			i = i + 1
			j = j + 1


		if((id_ant == max_tag_id) or (i > 39)):
			break
		else:
			id_ant = max_tag_id

		datos = api.tag_recent_media(tag_name = tag_name, max_tag_id = max_tag_id)
	

	id = 1034466
	i = 0

	posts = ""
	json_posts = ""
	next_link = ""
	lista_jsons = ""
	cargado_post = False

	datos = api.user_recent_media(user_id = id)

	id_ant = ""

	while (True):

		cargado_post = False
		for item in datos:
		
			tipo = str(type(item))
			#print tipo
			
			if (("list" in tipo) and (not(cargado_post))):
				posts = item
				cargado_post = True
			elif ("str" in tipo):
				json_posts = item
			elif ("unicode" in tipo):
				next_link = item
			elif(("list" in tipo) and (cargado_post)):
				lista_jsons = item

		inicio = next_link.find("max_id=")
		inicio = inicio + 7
		max_id = next_link[inicio:]

		#print json_posts
		j = 0
		for item in posts:
			print str(i) + ") " + str(item)
			print item.id

			if(hasattr(item.caption,'text')):
				print item.caption.text
		
			print item.link
			print lista_jsons[j]
			print
			print to_CSV(item)
			print
			i = i + 1
			j = j + 1

		if((id_ant == max_id) or (i > 39)):
			break
		else:
			id_ant = max_id

		datos = api.user_recent_media(user_id = id, max_id = max_id)

	


	#id = 1034466
	#id = 380142891

	#print id

"""


"""
	tag_name = "peru"

	datos = api.tag_recent_media(tag_name = tag_name)

	posts = ""
	json_posts = ""
	next_link = ""
	cargado_post = False
	lista_jsons = ""

	for item in datos:
			
			tipo =  str(type(item))
			print tipo
			
			if (("list" in tipo) and (not(cargado_post))):
				posts = item
				cargado_post = True
			elif ("str" in tipo):
				json_posts = item
			elif ("unicode" in tipo):
				next_link = item
			elif(("list" in tipo) and (cargado_post)):
				lista_jsons = item



	for item in lista_jsons:
		print
		print item
		print

	#print json_posts
"""


"""


	tag_name = "peru"

	datos = api.tag_recent_media(tag_name = tag_name)

	posts = ""
	json_posts = ""
	next_link = ""
	cargado_post = False
	lista_jsons = ""

	for item in datos:
			
			tipo =  str(type(item))
			print tipo
			
			if (("list" in tipo) and (not(cargado_post))):
				posts = item
				cargado_post = True
			elif ("str" in tipo):
				json_posts = item
			elif ("unicode" in tipo):
				next_link = item
			elif(("list" in tipo) and (cargado_post)):
				lista_jsons = item


	#for item in posts:
	#	to_CSV(item)
	
	#print json_posts
"""





