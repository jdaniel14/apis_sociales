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

# Variables globares
CANT_TWEETS = 20

#Para poder obtener el json. No funciona en Lists ni Cursors
class MyModelParser(tweepy.parsers.ModelParser):
    def parse(self, method, payload):
        result = super(MyModelParser, self).parse(method, payload)
        result._payload = json2.loads(payload)
        return result


#Clases propias

class MetadataPersonalizado(object):
	iso_language_code = ""
	result_type = ""

	def __init__(self,**metadatos):
		self.iso_language_code = metadatos['iso_language_code']
		self.result_type = metadatos['result_type']


class HastTagsPersonalizado(object):
	text = ""
	indices = []

	def __init__(self,hashes):
		
		self.text = hashes['text']
		self.indices = (hashes['indices'][0], hashes['indices'][1])
		#indices = []

		#for ind in hashes['indices']:
		#	self.indices.append(ind)

class URLPersonalizado(object):
	display_url = ""
	expanded_url = ""
	url = ""
	indices = []

	def __init__(self,links):
		self.display_url = links['display_url']
		self.expanded_url = links['expanded_url']
		self.url = links['url']
		self.indices = (links['indices'][0], links['indices'][1])


class UsuarioMencionadoPersonalizado(object):
	id = 0
	id_str = ""
	name = ""
	screen_name = ""
	indices = []

	def __init__(self,usuariomencionado):
		self.id = usuariomencionado['id']
		self.id_str = usuariomencionado['id_str']
		self.name = usuariomencionado['name']
		self.screen_name = usuariomencionado['screen_name']
		self.indices = (usuariomencionado['indices'][0], usuariomencionado['indices'][1])

class MediaPersonalizado(object):
	id = 0
	id_str = ""
	expanded_url = ""
	display_url = ""
	url = ""
	type = ""
	media_url = ""
	indices = []

	def __init__(self,mediausuario):
		self.id = mediausuario['id']
		self.id_str = mediausuario['id_str']
		self.expanded_url = mediausuario['expanded_url']
		self.display_url = mediausuario['display_url']
		self.url = mediausuario['url']
		self.type = mediausuario['type']
		self.media_url = mediausuario['media_url']
		self.indices = (mediausuario['indices'][0], mediausuario['indices'][1])

class EntitiesPersonalizado(object):
	urls = []
	hashtags = []
	user_mentions = []
	media = []


	def __init__(self,entidades,entidades_extendidos = {}):
		
		self.urls = []
		self.hashtags = []
		self.user_mentions = []
		self.media = []

		if entidades.has_key('urls'):
			for url in entidades['urls']:
				temp = URLPersonalizado(url)
				self.urls.append(temp)

		if entidades.has_key('hashtags'):
			for tag in entidades['hashtags']:
				temp = HastTagsPersonalizado(tag)
				self.hashtags.append(temp)


		if entidades.has_key('user_mentions'):
			for user_m in entidades['user_mentions']:
				temp = UsuarioMencionadoPersonalizado(user_m)
				self.user_mentions.append(temp)

		if entidades.has_key('media'):
			for media_es in entidades['media']:
				temp = MediaPersonalizado(media_es)
				self.media.append(temp)



"""
class DescriptionPersonalizado(object):
	urls = []

	def __init__(self,**valores):
		pass
"""

class UsuarioPersonalizado(object):
	id = 0
	name = ""
	url = ""
	created_at = ""
	location = ""
	statuses_count = 0
	friends_count = 0
	following = False
	screen_name = ""
	description = ""
	#favorites_count = 0
	lang = ""
	followers_count = 0
	time_zone = ""

	default_profile_image = False
	profile_image_url = ""
	profile_use_background_image = False
	profile_background_image_url = ""

	notifications = False

	entities = ""

	#descriptions = DescriptionPersonalizado()

	utc_offset = 0
	protected = False
	verified = False
	geo_enabled = False
	show_all_inline_media = False

	def __init__(self,usuario):
		self.id = usuario.id
		self.name = usuario.name
		self.url = usuario.url
		self.created_at = str(usuario.created_at)
		self.location = usuario.location
		self.statuses_count = usuario.statuses_count
		self.friends_count = usuario.friends_count
		self.following = usuario.following
		self.screen_name = usuario.screen_name
		self.description = usuario.description
		
		#self.favorites_count = usuario.favorites_count
		
		self.lang = usuario.lang
		self.followers_count = usuario.followers_count
		self.time_zone = usuario.time_zone

		self.default_profile_image = usuario.default_profile_image
		self.profile_image_url = usuario.profile_image_url
		self.profile_use_background_image = usuario.profile_use_background_image
		self.profile_background_image_url = usuario.profile_background_image_url

		self.notifications = usuario.notifications

		self.entities = EntitiesPersonalizado(usuario.entities)

		#self.descriptions = DescriptionPersonalizado(usuario.)

		self.utc_offset = usuario.utc_offset
		self.protected = usuario.protected
		self.verified = usuario.verified
		self.geo_enabled = usuario.geo_enabled
		
		#self.show_all_inline_media = usuario.show_all_inline_media


class StatusPersonalizado(object):
	id = 0
	id_str = ""
	source = ""
	geo = ""
	place = ""
	text = ""

	metadata = ""

	retweet_count = 0
	retweeted = False
	coordinates = ""
	favorited = False
	favorite_count = 0
	truncated = False
	created_at = ""

	entities = ""
	extended_entities = []

	user = ""

	in_reply_to_user_id = 0
	in_reply_to_user_id_str = ""
	in_reply_to_status_id = 0
	in_reply_to_status_id_str = ""
	in_reply_to_screen_name = ""


	def __init__(self,posteo):
		
		self.id = posteo.id
		self.id_str = posteo.id_str
		self.source = posteo.source
		
		#self.geo = posteo.geo
		#self.place = posteo.place
		#self.coordinates = posteo.coordinates
		self.geo = "null"
		self.place = "null"
		self.coordinates = "null"

		self.text = posteo.text

		self.metadata = MetadataPersonalizado(iso_language_code = posteo.lang, result_type = "")

		self.retweet_count = posteo.retweet_count
		if hasattr(posteo, "retweeted_status"):
			self.retweeted 	= True
		
		self.favorited = posteo.favorited
		self.favorite_count = posteo.favorite_count
		self.truncated = posteo.truncated
		self.created_at = str(posteo.created_at)

		if hasattr(posteo, "extended_entities"):
			self.extended_entities = posteo.extended_entities




		self.entities = EntitiesPersonalizado(posteo.entities)

		self.user = UsuarioPersonalizado(posteo.user)

		self.in_reply_to_user_id = posteo.in_reply_to_user_id
		self.in_reply_to_user_id_str = posteo.in_reply_to_user_id_str
		self.in_reply_to_status_id = posteo.in_reply_to_status_id
		self.in_reply_to_status_id_str = posteo.in_reply_to_status_id_str
		self.in_reply_to_screen_name = posteo.in_reply_to_screen_name

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def to_JSON_one_line(self):
		jsonconv = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent = 4)

		jsonconv = jsonconv.replace('\n','')
		jsonconv = jsonconv.replace('  ','')
		jsonconv = jsonconv.replace('   ','')
		jsonconv = jsonconv.replace('    ','')
		jsonconv = jsonconv.replace('     ','')
		jsonconv = jsonconv.replace('      ','')
		jsonconv = jsonconv.replace('       ','')

		texto = json2.dumps(jsonconv, separators=(',',':'), sort_keys=True)

		texto = texto.decode('string_escape')
		texto = texto[1:-1]
		return texto

	def to_CSV(self):
		head = ""

		head += str(self.id) + "|"
		head += str(self.id_str) + "|"
		head += self.source + "|"
		head += self.geo + "|"
		head += self.place + "|"
		head += self.text + "|"

		head += self.metadata.iso_language_code + "|"

		head += str(self.retweet_count) + "|"
		head += str(self.retweeted) + "|"
		head += str(self.coordinates) + "|"
		head += str(self.favorited) + "|"
		head += str(self.favorite_count) + "|"
		head += str(self.truncated) + "|"
		head += str(self.created_at) + "|"

		for item in self.entities.urls:
			head += str(item.expanded_url) + "!!"

		head = head[:-2]

		head += "|"

		head += str(self.user.id) + "|"
		head += self.user.screen_name + "|"
		head += self.user.name + "|"
		head += str(self.user.url) + "|"
		head += str(self.user.profile_image_url) + "|"

		head += str(self.in_reply_to_user_id) + "|"
		head += str(self.in_reply_to_user_id_str) + "|"
		head += str(self.in_reply_to_status_id) + "|"
		head += str(self.in_reply_to_status_id_str) + "|"
		head += str(self.in_reply_to_screen_name) + "\n"


		return head.encode('utf-8')




def CSV_header():
		
	head = ""

	head += "id|"
	head += "id_str|"
	head += "source|"
	head += "geo|"
	head += "place|"
	head += "text|"

	head += "iso_language_code"

	head += "|"

	head += "retweet_count|"
	head += "retweeted|"
	head += "coordinates|"
	head += "favorited|"
	head += "favorite_count|"
	head += "truncated|"
	head += "created_at|"

	head += "urls"

	head += "|"

	head += "user_id"

	head += "|"

	head += "user_screen_name|"

	head += "user_url|"

	head += "user_profile_image_url|"

	head += "in_reply_to_user_id|"
	head += "in_reply_to_user_id_str|"
	head += "in_reply_to_status_id|"
	head += "in_reply_to_status_id_str|"
	head += "in_reply_to_screen_name\n"

	return head.encode('utf-8')	

