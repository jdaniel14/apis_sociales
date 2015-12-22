# -*- coding: utf-8 -*-

import tweepy
from tweepy import Cursor
import simplejson as json2
import csv
import datetime
import json
import sys
from classes import *

CANT_TWEETS	= 20


def main():
	
	next_begin	= 0

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


	f_publicacion 	= open(NOMBRE_ARCHIVO_SALIDA1,	'wb')
	f_opinion 		= open(NOMBRE_ARCHIVO_SALIDA2,	'wb')
	#escritorcsv 	= open('posts.csv','w')

	with open(NOMBRE_ARCHIVO_ENTRADA,'r') as f:
		lines 	= f.readlines()

	usuarios 	= []
	tags 		= []
	sinces 		= []

	for item in lines:
		linea 	= item.split(';')
		sinces.append	(linea[3])
		usuarios.append	(linea[0])
		tags.append		(linea[7].split(','))

	print "** Inicio Datos para leer **"

	print usuarios
	print tags

	print "** Fin Datos para leer **"

	auth	= tweepy.OAuthHandler('2L6jkxYvo7tCZsi48Bu6hGFFt', 'S7vLdLhhfWSsE8c5QVW3eVRXFS02OQRh2GQABurCG3kjeiqxEV')
	auth.set_access_token('393819808-JQa3Flxu0e43qErgm3zt7iRetREqvdbpkBRmrnzK', 'ffSh4Ra9QpPo8T4JLl03V664MCQj8pIzO2zd3cbXTrqt1')

	api 	= tweepy.API(auth,parser=MyModelParser())

	c	= 0 #Linea que se esta leyendo

	for inusuario in usuarios:

		next_begin 	= 0

		user 		= api.get_user(inusuario)

		print "@" + user.screen_name
		print '\n'

		f_publicacion.write(inusuario + "\n")
		f_opinion.write(inusuario + "\n")

		if (sinces[c] == "0"):
			SINCE_ID_VAR	= None
		else:
			SINCE_ID_VAR	= sinces[c]


		for status in Cursor(api.user_timeline, user.id, since_id = SINCE_ID_VAR).items(CANT_TWEETS):

			tweetGuardar	= StatusPersonalizado(status) # **** GUARDAR TWEET

			if (tweetGuardar.id > next_begin):
				next_begin	= tweetGuardar.id

			print tweetGuardar.id
			print tweetGuardar.text
			print tweetGuardar.created_at
			print '\n'


			print tweetGuardar.to_JSON_one_line()
			print
			print


			f_publicacion.write(tweetGuardar.to_JSON_one_line())
			f_publicacion.write('\n')

		tagsuser = tags[c] #los tags que estan para el correspondiente usuario

		print tagsuser

		for intag in tagsuser:
			intag = intag.rstrip('\n')
			print intag
			print '\n'

			f_opinion.write(intag + "\n")

			for tweets in Cursor(api.search, q=intag, since_id=SINCE_ID_VAR).items(CANT_TWEETS):

				tweetGuardar 	= StatusPersonalizado(tweets) # **** GUARDAR TWEET

				if (tweetGuardar.id > next_begin):
					next_begin 	= tweetGuardar.id

				print tweetGuardar.id
				print tweetGuardar.id_str
				print tweets.text
				print str(tweets.created_at)
				print '\n';

				print tweetGuardar.to_JSON_one_line()

				f_opinion.write(tweetGuardar.to_JSON_one_line())
				f_opinion.write('\n')

		if (next_begin == 0):
			next_begin = SINCE_ID_VAR

		f_publicacion.write("!@#END\n")
		f_opinion.write("!@#END\n")
		f_publicacion.write(str(next_begin) + "\n")
		f_opinion.write(str(next_begin) + "\n")

		print "!@#END"
		print next_begin

		c = c + 1

	print "\n"

	f_publicacion.close()
	f_opinion.close()

main()
