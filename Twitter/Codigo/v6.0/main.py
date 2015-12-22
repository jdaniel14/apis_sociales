# -*- coding: utf-8 -*-

# python
# python main.py NOMBRE_ARCHIVO_ENTRADA NOMBRE_ARCHIVO_SALIDA1(Publicaciones) NOMBRE_ARCHIVO_SALIDA2(Opiniones) 
# se le tiene que pasar el ID del post desde el cual se quiere obtener los datos
# se comprueba manualmente que no se repite ese tweet
# se devuelve el tweet a partir del cual se debe obtener los datos (ese ultimo es excluido manualmente

#Tweepy
import tweepy
from tweepy import Cursor

#Json
import simplejson as json2

#CVS file
import csv

#Time
import datetime

#Json
import json

import sys

from classes import *
# Variables globares
CANT_TWEETS = 20


def main():
	
	next_begin = 0

	# Lectura de Parametros

	print sys.argv

	try:
		NOMBRE_ARCHIVO_ENTRADA = str(sys.argv[1])

		if(NOMBRE_ARCHIVO_ENTRADA == ""):
			NOMBRE_ARCHIVO_ENTRADA = "../../../input.csv"
	except:
		NOMBRE_ARCHIVO_ENTRADA = "../../../input.csv"

	try:	
		NOMBRE_ARCHIVO_SALIDA1 = str(sys.argv[2])

		if(NOMBRE_ARCHIVO_SALIDA1 == ""):
			NOMBRE_ARCHIVO_SALIDA1 = "pe_twt_down_publicacion_fecha_hora.txt"
				
	except:
		NOMBRE_ARCHIVO_SALIDA1 = "pe_twt_down_publicacion_fecha_hora.txt"


	try:	
		NOMBRE_ARCHIVO_SALIDA2 = str(sys.argv[3])

		if(NOMBRE_ARCHIVO_SALIDA2 == ""):
			NOMBRE_ARCHIVO_SALIDA2 = "pe_twt_down_opinion_fecha_hora.txt"
				
	except:
		NOMBRE_ARCHIVO_SALIDA2 = "pe_twt_down_opinion_fecha_hora.txt"
	

	print "NOMBRE_ARCHIVO_ENTRADA: " + NOMBRE_ARCHIVO_ENTRADA
	print "NOMBRE_ARCHIVO_SALIDA1: " + NOMBRE_ARCHIVO_SALIDA1
	print "NOMBRE_ARCHIVO_SALIDA2: " + NOMBRE_ARCHIVO_SALIDA2


	escritorPublicacion = open(NOMBRE_ARCHIVO_SALIDA1,'w')
	escritorOpinion = open(NOMBRE_ARCHIVO_SALIDA2,'w')
	escritorcsv = open ('posts.csv','w')

	with open(NOMBRE_ARCHIVO_ENTRADA,'r') as f:
		lines = f.readlines()

	usuarios = []
	tags = []
	sinces = []

	for item in lines:
		linea = item.split(';')
		sinces.append(linea[3])
		usuarios.append(linea[0])
		tags.append(linea[7].split(','))

	print "** Inicio Datos para leer **"

	print usuarios
	print tags

	print "** Fin Datos para leer **"
		
	# Autorizacion de los datos de tweepy

	auth = tweepy.OAuthHandler('2L6jkxYvo7tCZsi48Bu6hGFFt', 'S7vLdLhhfWSsE8c5QVW3eVRXFS02OQRh2GQABurCG3kjeiqxEV')
	auth.set_access_token('393819808-JQa3Flxu0e43qErgm3zt7iRetREqvdbpkBRmrnzK', 'ffSh4Ra9QpPo8T4JLl03V664MCQj8pIzO2zd3cbXTrqt1')

	api = tweepy.API(auth,parser=MyModelParser())

	#results = api.user_timeline("@wilchess26") #logra como maximo 100 tweets

	#print json.dumps(results._payload) #para imprimir el json y ver mejor los campos



	#results = api.user_timeline("@wilchess26") #logra como maximo 100 tweets

	#print json.dumps(results._payload) #para imprimir el json y ver mejor los campos



	c = 0 #Linea que se esta leyendo

	escritorcsv.write(CSV_header())
				

	for inusuario in usuarios:

		next_begin = 0

		user = api.get_user(inusuario)

		print "@" + user.screen_name
		print '\n'

		escritorPublicacion.write(inusuario + "\n")
		escritorOpinion.write(inusuario + "\n")

		escritorcsv.write(inusuario + "\n")

		if (sinces[c] == "0"):
			SINCE_ID_VAR = None
		else:
			SINCE_ID_VAR = sinces[c]


		for status in Cursor(api.user_timeline, user.id, since_id = SINCE_ID_VAR).items(CANT_TWEETS):

			tweetGuardar = StatusPersonalizado(status) # **** GUARDAR TWEET

			if (tweetGuardar.id > next_begin):
				next_begin = tweetGuardar.id

			print tweetGuardar.id
			print tweetGuardar.text
			#fecha = status.created_at - datetime.timedelta(hours=5)
			#tweetGuardar.created_at = fecha
			print tweetGuardar.created_at
			print '\n'


			print tweetGuardar.to_JSON_one_line()
			print
			print


			escritorPublicacion.write(tweetGuardar.to_JSON_one_line())
			escritorPublicacion.write('\n')

			escritorcsv.write(tweetGuardar.to_CSV())

		tagsuser = tags[c] #los tags que estan para el correspondiente usuario

		print tagsuser

		for intag in tagsuser:
			intag = intag.rstrip('\n')
			print intag
			print '\n'

			escritorOpinion.write(intag + "\n")
			escritorcsv.write(intag + "\n")

			for tweets in Cursor(api.search, q=intag, since_id=SINCE_ID_VAR).items(CANT_TWEETS):

				tweetGuardar = StatusPersonalizado(tweets) # **** GUARDAR TWEET

				if (tweetGuardar.id > next_begin):
					next_begin = tweetGuardar.id

				print tweetGuardar.id
				print tweetGuardar.id_str
				print tweets.text
				print str(tweets.created_at)
				print '\n';

				print tweetGuardar.to_JSON_one_line()

				escritorOpinion.write(tweetGuardar.to_JSON_one_line())
				escritorOpinion.write('\n')

				escritorcsv.write(tweetGuardar.to_CSV())

		if (next_begin == 0):
			next_begin = SINCE_ID_VAR

		escritorPublicacion.write("!@#END\n")
		escritorOpinion.write("!@#END\n")
		escritorPublicacion.write(str(next_begin) + "\n")
		escritorOpinion.write(str(next_begin) + "\n")

		print "!@#END"
		print next_begin


		c = c + 1


	print "\n"

	

	escritorPublicacion.close()
	escritorOpinion.close()
	escritorcsv.close()

main()
