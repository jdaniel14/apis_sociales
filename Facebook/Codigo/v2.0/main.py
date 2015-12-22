# -*- coding: utf-8 -*-

# python
# python main.py NOMBRE_ARCHIVO_ENTRADA NOMBRE_ARCHIVO_SALIDA SINCE_ID_VAR
# En SINCE_ID_VAR se le debe pasar la fecha hasta la que quiere en epoch (fecha linux)
# Se devuelve al final la fecha en la que se realizo el proceso para que la siguiente
# se realice a partir de esa fecha

import facebook
import json

import simplejson as json2

import sys
from datetime import datetime

import time

CANT_LLAMADAS = 6
CANT_POSTS = 50
FORMAT_DATE = '%Y-%m-%dT%H:%M:%S'

def pp(o): 
    return json.dumps(o, indent=1)

def json_one_line(o):
	json_aux = json.dumps(o, indent=1)
	json_aux = json_aux.replace('\n','')
	json_aux = json_aux.replace('       ','')
	json_aux = json_aux.replace('      ','')
	json_aux = json_aux.replace('     ','')
	json_aux = json_aux.replace('    ','')
	json_aux = json_aux.replace('   ','')
	json_aux = json_aux.replace('  ','')

	texto = json2.dumps(json_aux, separators=(',',':'), sort_keys=True)

	texto = texto.decode('string_escape')
	texto = texto[1:-1]

	return texto


def main():


	next_begin = int(time.time())


	# Inicializacion de variables con los parametros


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
			NOMBRE_ARCHIVO_SALIDA = "postsFacebook.txt"
				
	except:
		NOMBRE_ARCHIVO_SALIDA = "postsFacebook.txt"

	try:	
		SINCE_ID_VAR = str(sys.argv[3])
	except:
		SINCE_ID_VAR = ""

	print "NOMBRE_ARCHIVO_ENTRADA: " + NOMBRE_ARCHIVO_ENTRADA
	print "NOMBRE_ARCHIVO_SALIDA: " + NOMBRE_ARCHIVO_SALIDA
	print "SINCE_ID_VAR: " + SINCE_ID_VAR

	#token online
	#token = "CAAEWP2tWTywBAH2QO2nd3bCwZCyBFexLmG9inZCgiLwXZAEHZCWTmmHBxoZCDDJ4fNCDkZAzNxygt6BHMYMOweVBXTCgOWFMO4dZAHuZCD7Oelo5M9D8mIjZAUYmIkeoCEHP8hAZAQfRMwIWGssuJDehA5CajSeMV7OOQKcds8Wq5uUoj07exG37jqW05XW69rcaC5SwLIQuhEUZBU9tlZA4v2qs"

	#token del console
	token = "CAACEdEose0cBAAsIhIJw1xWzQfXyRk46OhFHT4CIZBr3qDjvA0YGVpeKZBKnLLOudICRFtOYMrp01EicIvSfW2yoZBbfkwJFky0FVgGnbYXmaKkvDz4IWNmbr6UBDyGpik6sZB9yRCXmyWnGzy2DGMbufpW0vJYLrZCxkRlXIxADY8Vt8Lfu4UWQobuGvsCJx9cLMzcR8kdNxXlYffEgghjvMVFeJZBM8ZD"
	graph = facebook.GraphAPI(token)


	escritor = open(NOMBRE_ARCHIVO_SALIDA,'w')



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




	c = 0 #Linea que se esta leyendo



	for inusuario in usuarios:

		print "user: " + inusuario
		print '\n'

		escritor.write("@" + str(inusuario) + "\n")
		
		id = inusuario

		profile = graph.get_object(id)

		i = 0
		next_until = ''

		while (True):

			#1324924606

			posts = graph.get_connections(profile['id'], 'posts', until=next_until, since=SINCE_ID_VAR)

			#print pp(posts).replace('\n','')

			# Obtengo el until que me permita navegar a la siguiente coleccion de posts
			
			if (posts.has_key('paging')):
				pass
			else:
				break

			next_until = posts['paging']['next']
			inicio = next_until.find("until=")
			inicio = inicio + 6
			next_until = next_until[inicio:]


			for item in posts['data']:

				print str(i) +  ")"

				post_json = json_one_line(item)
				print
				print post_json
				print

				escritor.write(post_json)
				escritor.write('\n')

				i = i + 1

			if (i >= CANT_POSTS):
				break




		tagsuser = tags[c] #los tags que estan para el correspondiente usuario

		print tagsuser

		for intag in tagsuser:
			intag = intag.rstrip('\n')

			print intag
			print '\n'

			escritor.write(intag + "\n")

			i = 0
			next_until = ''
			tag = intag

			while (True):
				#1412214991
				#La cantidad que devuelve depende del usuario o tag

				posttag = graph.request("search", {'q' : tag , 'type' : 'post', 'limit':'25', 'until':next_until, 'since':SINCE_ID_VAR})

				if (posttag.has_key('paging')):
					pass
				else:
					break

				# Obtengo el until que me permita navegar a la siguiente coleccion de posts
				next_until = posttag['paging']['next']
				inicio = next_until.find("until=")
				inicio = inicio + 6
				next_until = next_until[inicio:]

				# Recorro todos los posts
				for item in posttag['data']:

					print str(i) +  ")"

					post_json = json_one_line(item)
					print
					print post_json
					print

					escritor.write(post_json)
					escritor.write('\n')


					i = i + 1

				if( i >= CANT_POSTS):
					break



		c = c + 1

	finfinfin = "!@#END\n"
	escritor.write(finfinfin)
	escritor.write(str(next_begin))


	if (next_begin == 0):
		next_begin = SINCE_ID_VAR


	print "!@#END"
	print next_begin
	escritor.write("\n")

	escritor.close()



main()


