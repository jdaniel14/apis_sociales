# -*- coding: utf-8 -*-

# python
# python main.py NOMBRE_ARCHIVO_ENTRADA NOMBRE_ARCHIVO_SALIDA SINCE_ID_VAR
# se le tiene que pasar el ID del post desde el cual se quiere obtener los datos
# se comprueba manualmente que no se repite ese post
# se devuelve el post a partir del cual se debe obtener los datos (ese ultimo es excluido manualmente)

# Fuentes:
# http://pastebin.com/FtZ8MZ8f
# http://instagram.com/developer/endpoints/users/
# https://github.com/Instagram/python-instagram

import instagram

import unicodedata

import sys

def imprime_header_csv():
	head = ""

	head += "tags|"

	head += "user_id|"

	head += "user_username|"

	head += "user_screen_name|"

	head += "user_profile_image_url|"

	head += "videolow|"
	head += "videostd|"

	head += "imagelow|"
	head += "imagestd|"

	head += "link|"

	head += "created_at|"

	head += "text|"
	head += "caption_id|"

	head += "type|"

	head += "id|"

	head += "likes_count"

	head += "\n"

	return head.encode('utf-8')



def to_CSV(post):
	head = ""

	try:
		for item in post.tags:
			cadena = unicodedata.normalize('NFKD', item.name).encode('ascii','ignore')
			head += cadena + "!!"
	except:
		head += "Null!!"


	head = head[:-2]

	head += "|"

	head += str(post.user.id) + "|"

	head += str(post.user.username) + "|"

	head += str(post.user.profile_picture) + "|"

	try:
		head += str(post.videos["low_resolution"].url) + "|"
	except:
		head += "Null|"

	try:
		head += str(post.videos["standard_resolution"].url) + "|"
	except:
		head += "Null|"


	head += str(post.images["low_resolution"].url) + "|"
	head += str(post.images["standard_resolution"].url) + "|"

	head += str(post.link) + "|"

	head += str(post.created_time) + "|"


	try:
		aux = unicodedata.normalize('NFKD', post.caption.text).encode('ascii','ignore')
		aux = aux.replace('\n',' ')
		head += str(aux) + "|"
	except:
		head += "Null|"

	try:
		head += str(post.caption.id) + "|"
	except:
		head += "Null|"
	

	head += str(post.type) + "|"

	head += str(post.id) + "|"

	head += str(len(post.likes)) 

	head += "\n"

	return head.encode('utf-8')

	
def main():

	next_begin = ""

	# Lectura de datos de entrada

	print sys.argv

	try:
		NOMBRE_ARCHIVO_ENTRADA = str(sys.argv[1])

		if(NOMBRE_ARCHIVO_ENTRADA == ""):
			NOMBRE_ARCHIVO_ENTRADA = "input.csv"
	except:
		NOMBRE_ARCHIVO_ENTRADA = "input.csv"

	try:	
		NOMBRE_ARCHIVO_SALIDA = str(sys.argv[2])

		if(NOMBRE_ARCHIVO_SALIDA == ""):
			NOMBRE_ARCHIVO_SALIDA = "postsInstagram.txt"
	except:
		NOMBRE_ARCHIVO_SALIDA = "postsInstagram.txt"

	try:	
		SINCE_ID_VAR = str(sys.argv[3])
	except:
		SINCE_ID_VAR = ""

	print "NOMBRE_ARCHIVO_ENTRADA: " + NOMBRE_ARCHIVO_ENTRADA
	print "NOMBRE_ARCHIVO_SALIDA: " + NOMBRE_ARCHIVO_SALIDA
	print "SINCE_ID_VAR: " + SINCE_ID_VAR




	#print sys.argv

	access_token = "380142891.e8425be.67a8da3a5cbe4490b6702b4653a97137"
	client_id = "e8425beec7f74d3cb4bd27dddedf3f61"
	client_secret = "713cbd9a978641fc9bcc68abf209d11c"

	api = instagram.InstagramAPI(access_token=access_token)
	#api = instagram.InstagramAPI(client_id=client_id,client_secret=client_secret)

	print

	#sys.exit("Finalizado a la fuerza")

	escritor = open(NOMBRE_ARCHIVO_SALIDA,'w')
	escritorcsv = open ('posts.csv','w')

	with open(NOMBRE_ARCHIVO_ENTRADA,'r') as f:
		lines = f.readlines()

	usuarios = []
	tags = []

	for item in lines:
		linea = item.split(';')
		usuarios.append(linea[0])
		tags.append(linea[1].split(','))


	print "** Inicio Datos para leer **"

	print usuarios
	print tags

	print "** Fin Datos para leer **"


	escritorcsv.write(imprime_header_csv())

	c = 0 #Linea que se esta leyendo

	for inusuario in usuarios:

		print "user: " + inusuario
		print '\n'

		escritor.write("@" + str(inusuario) + "\n")
		escritorcsv.write("@" + str(inusuario) + "\n")
		
		######

		id = inusuario
		i = 0

		posts = ""
		json_posts = ""
		next_link = ""
		lista_jsons = ""
		cargado_post = False


		# Utilizo una variable propia para que no repita el SINCE_ID_VAR
		terminar_posts = False

		datos = api.user_recent_media(user_id = id, min_id = SINCE_ID_VAR)

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

			inicio = next_link.find("ma_id=")
			inicio = inicio + 7
			max_id = next_link[inicio:]

			#print json_posts
			j = 0
			for item in posts:

				if((SINCE_ID_VAR != "") and (str(item.id) <= SINCE_ID_VAR)):
					terminar_posts = True
					break

				if (item.id > next_begin):
					next_begin = str(item.id)

				print str(i) + ") " + str(item)
				print item.id

				if(hasattr(item.caption,'text')):
					print item.caption.text
			
				print item.link
				print lista_jsons[j]
				print
				print to_CSV(item)
				print

				escritor.write(lista_jsons[j])
				escritor.write('\n')
				escritorcsv.write(to_CSV(item))

				i = i + 1
				j = j + 1

			if(terminar_posts):
				break

			if((id_ant == max_id) or (i > 39)):
				break
			else:
				id_ant = max_id

			datos = api.user_recent_media(user_id = id, max_id = max_id, min_id = SINCE_ID_VAR)

		######

		tagsuser = tags[c] #los tags que estan para el correspondiente usuario

		print tagsuser

		#####

		for intag in tagsuser:
			intag = intag.rstrip('\n')

			print intag
			print '\n'

			escritor.write(intag + "\n")
			escritorcsv.write(intag + "\n")

			i = 0

			tag_name = intag[1:]

			posts = ""
			json_posts = ""
			next_link = ""
			lista_jsons = ""
			cargado_post = False

			# Deberia usarse el min_tag_id pero no sirve. http://instagram.com/developer/endpoints/tags/#
			# Se hara a la fuerza. Terminando cuando se encuentre uno que no cumple
			terminar = False


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
						#print json_posts
					elif ("unicode" in tipo):
						next_link = item
					elif(("list" in tipo) and (cargado_post)):
						lista_jsons = item


				inicio = next_link.find("max_tag_id=")
				inicio = inicio + 11
				max_tag_id = next_link[inicio:]

				j = 0
				for item in posts:
					
					if((SINCE_ID_VAR != "") and (str(item.id) <= SINCE_ID_VAR)):
						terminar = True
						break

					if(item.id > next_begin):
						next_begin = item.id

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

					escritor.write(lista_jsons[j])
					escritor.write('\n')

					escritorcsv.write(to_CSV(item))

					i = i + 1
					j = j + 1


				if (terminar):
					break

				if((id_ant == max_tag_id) or (i > 39)):
					break
				else:
					id_ant = max_tag_id

				datos = api.tag_recent_media(tag_name = tag_name, max_tag_id = max_tag_id)


		#####

		c = c + 1

	#results = api.user_timeline("@wilchess26") #logra como maximo 100 tweets

	#print json.dumps(results._payload) #para imprimir el json y ver mejor los campos

	print "\n"

	escritor.write("!@#END\n")
	escritor.write(str(next_begin))

	escritor.close()
	escritorcsv.close()

	if (next_begin == 0):
		next_begin = SINCE_ID_VAR

	print "!@#END"
	print next_begin



main()
