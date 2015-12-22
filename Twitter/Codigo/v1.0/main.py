# -*- coding: utf-8 -*-

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
import codecs

# Variables globares
CANT_TWEETS = 200

reload(sys)
sys.setdefaultencoding("utf-8")
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

#Para poder obtener el json. No funciona en Lists ni Cursors
class MyModelParser(tweepy.parsers.ModelParser):
	def parse(self, method, payload):
		result = super(MyModelParser, self).parse(method, payload)
		result._payload = json2.loads(payload)
		print "AQUI " + result.__class__.__name__
		if result.__class__.__name__ == "ResultSet":
			print len(result)
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
	#indices = []

	def __init__(self,hashes):
		
		self.text = hashes['text']

		#indices = []

		#for ind in hashes['indices']:
		#	self.indices.append(ind)

class URLPersonalizado(object):
	display_url = ""
	expanded_url = ""
	url = ""

	def __init__(self,links):
		self.display_url = links['display_url']
		self.expanded_url = links['expanded_url']
		self.url = links['url']


class UsuarioMencionadoPersonalizado(object):
	id = 0
	id_str = ""
	name = ""
	screen_name = ""

	def __init__(self,usuariomencionado):
		self.id = usuariomencionado['id']
		self.id_str = usuariomencionado['id_str']
		self.name = usuariomencionado['name']
		self.screen_name = usuariomencionado['screen_name']

class MediaPersonalizado(object):
	id = 0
	id_str = ""
	expanded_url = ""
	display_url = ""
	url = ""
	type = ""
	media_url = ""

	def __init__(self,mediausuario):
		self.id = mediausuario['id']
		self.id_str = mediausuario['id_str']
		self.expanded_url = mediausuario['expanded_url']
		self.display_url = mediausuario['display_url']
		self.url = mediausuario['url']
		self.type = mediausuario['type']
		self.media_url = mediausuario['media_url']

class EntitiesPersonalizado(object):
	urls = []
	hashtags = []
	user_mentions = []
	media = []


	def __init__(self,entidades):
		
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
	id 			= 0
	id_str 		= ""
	source 		= ""
	geo 		= ""
	place 		= ""
	text 		= ""

	metadata 	= ""

	retweet_count 	= 0
	retweeted 		= False
	coordinates 	= ""
	favorited 		= False
	favorite_count 	= 0
	truncated 		= False
	created_at 		= ""

	entities 			= ""
	extended_entities	= ""

	user 	= ""

	in_reply_to_user_id 		= 0
	in_reply_to_user_id_str 	= ""
	in_reply_to_status_id 		= 0
	in_reply_to_status_id_str 	= ""
	in_reply_to_screen_name 	= ""


	def __init__(self,posteo):
		
		self.id 	= posteo.id
		self.id_str = posteo.id_str
		self.source = posteo.source
		
		#self.geo = posteo.geo
		#self.place = posteo.place
		#self.coordinates = posteo.coordinates
		self.geo 			= "null"
		self.place 			= "null"
		self.coordinates 	= "null"

		self.text = posteo.text

		self.metadata = MetadataPersonalizado(iso_language_code = posteo.lang, result_type = "")

		self.retweet_count 	= posteo.retweet_count
		if hasattr(posteo, "retweeted_status"):
			self.retweeted 		= True
		
		self.favorited 		= posteo.favorited
		self.favorite_count = posteo.favorite_count
		self.truncated 		= posteo.truncated
		self.created_at 	= str(posteo.created_at)

		self.entities 			= EntitiesPersonalizado(posteo.entities)
		self.extended_entities	= None
		if hasattr(posteo, "extended_entities"): 
			self.extended_entities	= posteo.extended_entities

		self.user 	= UsuarioPersonalizado(posteo.user)

		self.in_reply_to_user_id 		= posteo.in_reply_to_user_id
		self.in_reply_to_user_id_str 	= posteo.in_reply_to_user_id_str
		self.in_reply_to_status_id 		= posteo.in_reply_to_status_id
		self.in_reply_to_status_id_str 	= posteo.in_reply_to_status_id_str
		self.in_reply_to_screen_name 	= posteo.in_reply_to_screen_name

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

class PostSalida:
	_id 					= None
	post_id					= None
	post_creation_date		= None
	post_network			= None
	post_source				= None
	post_url				= None
	post_text				= None
	post_language			= None
	post_hashtag			= None
	post_attach				= None
	post_retweeted			= None
	post_report_status		= None
	user_owner_id			= None
	user_owner_screen_name	= None
	user_owner_url			= None
	user_owner_images		= None
	

	def __init__(self, post):
		self.post_id				= post.id
		self.user_owner_id			= post.user.id
		self.post_creation_date		= post.created_at
		self.post_network			= 1 #debe salir del conf
		self.post_source			= post.source
		self.post_url				= "https://twitter.com/%s/status/%s"%(self.user_owner_id, self.post_id)
		self.post_text				= post.text
		self.post_language			= post.metadata.iso_language_code
		self.post_hashtag			= post.entities.hashtags
		self.post_attach			= post.entities.urls
		self.post_report_status		= 0 #debe salir del conf
		self.post_retweeted			= post.retweeted
		self.user_owner_name		= post.user.name
		self.user_owner_screen_name	= post.user.screen_name
		self.user_owner_url			= "https://twitter.com/%s"%(post.user.screen_name)
		self.user_owner_images		= post.user.profile_image_url

	def to_JSON(self):
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

def main():
	

	escritor = open('posts.txt','w')
	escritorcsv = open ('posts.csv','w')

	usuario_sys	= sys.argv[1]
	hashtag_sys	= sys.argv[2]

	usuarios 		= []
	ult_id_usuarios	= -1

	tags 			= []
	ult_id_tags		=-1

	if len(usuario_sys) > 0 :
		usuario_list	= usuario_sys.split("|")
		ult_id_usuarios	= int(usuario_list[0])
		usuarios		= usuario_list[1].split(",")

	if len(hashtag_sys) > 0 :
		tags_list		= hashtag_sys.split("|")
		ult_id_tags		= int(tags_list[0])
		tags			= tags_list[1].split(",")
	
	print ult_id_usuarios
	print usuarios

	print 

	print ult_id_tags
	print tags


	print "** Inicio Datos para leer **"
	print "** Fin Datos para leer **"
		
	auth = tweepy.OAuthHandler('2L6jkxYvo7tCZsi48Bu6hGFFt', 'S7vLdLhhfWSsE8c5QVW3eVRXFS02OQRh2GQABurCG3kjeiqxEV')
	auth.set_access_token('393819808-JQa3Flxu0e43qErgm3zt7iRetREqvdbpkBRmrnzK', 'ffSh4Ra9QpPo8T4JLl03V664MCQj8pIzO2zd3cbXTrqt1')

	api = tweepy.API(auth,parser=MyModelParser())

	#results = api.user_timeline("@jastuvilcaf") #logra como maximo 100 tweets

	#params	= {}
	#params["since_id"]  = 418137264557154200
	#params["count"]		= 1
	#results = api.mentions_timeline("@theknifemadrid", parameters = params) #logra como maximo 100 tweets
	#results = api.mentions_timeline( parameters = params) #logra como maximo 100 tweets

	#api.mentions()

	#print json.dumps(results._payload) #para imprimir el json y ver mejor los campos

	c = 0 #Linea que se esta leyendo

	escritorcsv.write(CSV_header())
				

	for inusuario in usuarios:
		user = api.get_user(inusuario)

		print "@" + user.screen_name
		print '\n'

		#escritor.write(inusuario + "\n")
		#escritorcsv.write(inusuario + "\n")

		if ult_id_tags != -1:
			cursor	= Cursor(api.user_timeline, user.id).items(CANT_TWEETS)
		else : 
			cursor	= Cursor(api.user_timeline, user.id, since_id = ult_id_usuarios).items(CANT_TWEETS)

		for status in cursor :
			tweetGuardar = StatusPersonalizado(status) # **** GUARDAR TWEET
			if tweetGuardar.in_reply_to_user_id :
				continue
			
			flag_usuario_mencionado	= False
			if tweetGuardar.retweeted:
				#print "**********************************"
				for mention	in tweetGuardar.entities.user_mentions:
					busq	= mention.screen_name	
					print busq
					if busq == user.screen_name:
						flag_usuario_mencionado	= True
						break
						#print "AQUIIIIIIIIIIIIIIIIIIIIIII"
				#print "**********************************"
				if not flag_usuario_mencionado:
					continue

			print tweetGuardar.id
			print tweetGuardar.text
			print tweetGuardar.source
			#fecha = status.created_at - datetime.timedelta(hours=5)
			#tweetGuardar.created_at = fecha
			print tweetGuardar.created_at
			
			obj_ext	= tweetGuardar.extended_entities
			if obj_ext:
				for url in obj_ext["media"]:
					print "-----------> " + url["media_url"]
			#print '\n'
			#print tweetGuardar.to_JSON_one_line()
			#print
			#print status
			post_salida	= PostSalida(tweetGuardar)
			print post_salida.to_JSON()
			#escritor.write(tweetGuardar.to_JSON_one_line())
			#escritor.write(post_salida.to_JSON())
			print "----------------------------------------------------------------------"
			print json.dumps(status._json, ensure_ascii=False) 
			escritor.write('\n')
			#break
			#escritorcsv.write(tweetGuardar.to_CSV())

	print "\n"

	escritor.close()
	escritorcsv.close()

main()
