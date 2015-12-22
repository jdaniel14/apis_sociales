
import json

import simplejson as json2

import pprint


class MediaGeneral:
	def __init__(self):
		hashtags = None


class MediaTwitter:
	def __init__(self):
		urls = None
		media = None
		user_mentions = None


class MediaInstagram:
	def __init__(self):
		typeMedia = None
		images = None
		videos = None

class MediaFacebook:
	def __init__(self):
		typeMedia = None
		images = None
		videos = None


class PostConsolidado:
	def __init__(self):
		idNumber 		= None
		idString 		= None
		creation_date 	= None
		iso_language_code = None
		mediaGeneral = MediaGeneral()
		mediaTwitter = MediaTwitter()
		mediaInstagram = MediaInstagram()
		mediaFacebook = MediaFacebook()
		network = None
		source = None
		urlPost = None
		report_status = None
		text = None
		user_owner = None


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
		return texto + "\n"





"""
class Media:
	def __init__(self):
		hashtags		= None
		user_mentions	= None
		extern_links	= None
		photo_loaded	= None
		video_loaded	= None

class Post:
	def __init__(self):
		self.post_id			= None
		self.post_creation_date	= None
		self.post_network		= None
		self.post_url			= None
		self.post_text			= None
		self.post_media			= Media()
		self.post_report_status	= None
		#self.post_user_owner	= None

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
		return texto + "\n"
"""


def mainTwitter(escritor):

	with open("postsTwitter.txt",'r') as f:
		lines = f.readlines()

	for line in lines:
		
		if ((line[0] == '@') or (line[0] == '#')):
			print line
			#escritor.write(line);
		elif (line[0] == '{'):

			var_json	= json.loads(line)


			if(("Instagram" in var_json["source"]) or ("Facebook" in var_json["source"])):
				print "ELIMINADO"
				print "------------"
				print
				continue


			#Analisis de Retweeteado
			retweeted 	= False

			if "retweeted_status" in var_json.keys():
				retweeted      = True

			if var_json["in_reply_to_user_id"] :
				continue

			flag_usuario_mencionado = False
			if retweeted:
				for mention in var_json["entities"]["user_mentions"]:
					busq    = mention["screen_name"]
					if busq == var_json["user"]["screen_name"]:
						flag_usuario_mencionado = True
						break
				if not flag_usuario_mencionado:
					continue

			if flag_usuario_mencionado :
				var_json	= var_json["retweeted_status"]
			#Fin Analisis de Retweeteado

			pub			= PostConsolidado() 
			pub.idNumber			= var_json["id"]
			pub.idString			= var_json["id_str"]
			pub.creation_date	= 	var_json["created_at"]
			pub.iso_language_code = var_json["metadata"]["iso_language_code"]

			#seccion del user
			id				= var_json["user"]["id"]
			nameShort	= var_json["user"]["screen_name"]
			nameLong			= var_json["user"]["name"]
			#user_url			= "https://twitter.com/%s"%(user_screen_name)	
			profile_background_image_url = var_json["user"]["profile_background_image_url"]
			profile_image_url = var_json["user"]["profile_image_url"]

			pub.user_owner	= {
				"id" : id, "nameLong" : nameLong, "nameShort" : nameShort, "profile_background_image_url" : profile_background_image_url,
				"profile_image_url" : profile_image_url
			}
			
			pub.network = 1
			pub.source		= var_json["source"]
			pub.urlPost		= "https://twitter.com/%s/status/%s"%(nameShort, pub.idNumber)
			pub.report_status = 0
			pub.text			= var_json["text"]
			
			print pub.idNumber
			print pub.urlPost

			list_hashtags		= []
			pub.mediaGeneral = MediaGeneral()

			if "hashtags" in var_json["entities"].keys() :
				for hashtag in var_json["entities"]["hashtags"]:
					indices	= (hashtag["indices"][0], hashtag["indices"][1])
					text	= hashtag["text"]
					list_hashtags.append({"text":text, "indices":indices})
				pub.mediaGeneral.hashtags = list_hashtags

			pub.mediaTwitter = MediaTwitter()
			list_user_mentions	= []
			if "user_mentions" in var_json["entities"].keys() :
				for user_mention in var_json["entities"]["user_mentions"]:
					id_user_mention = user_mention["id"]
					id_str_user_mention = user_mention["id_str"]
					indices	= (user_mention["indices"][0], user_mention["indices"][1])
					name_user_mention = user_mention["name"]
					screen_name_user_mention	= user_mention["screen_name"]
					list_user_mentions.append({"id": id_user_mention, "id_str": id_str_user_mention, "indices":indices, 
											"name": name_user_mention, "screen_name":text})
				pub.mediaTwitter.user_mentions = list_user_mentions

			list_links			= []
			if "urls" in var_json["entities"].keys() :
				for link in var_json["entities"]["urls"]:
					display_url = link["display_url"]
					expanded_url	= link["expanded_url"]
					url = link["url"]
					indices	= (link["indices"][0], link["indices"][1])
					list_links.append({"display_url":display_url, "expanded_url": expanded_url, "url":url, "indices":indices})
				pub.mediaTwitter.urls = list_links


			"""
			if "media" in var_json["entities"].keys():
				for link in var_json["entities"]["media"]:
					indices	= (link["indices"][0], link["indices"][1])
					text	= link["expanded_url"]
					list_links.append({"extended_url":text, "indices":indices})
				pub.mediaTwitter.urls = list_links
			"""

			photo_loaded		= []
			
			#if "media" in var_json["entities"].keys():
			if "extended_entities" in var_json:
			#	for link in var_json["entities"]["media"]:
				for link in var_json["extended_entities"]["media"]:
					id = link["id"]
					display_url = link["display_url"]
					expanded_url = link["expanded_url"]
					media_url = link["media_url"]
					media_url_https = link["media_url_https"]
					url = link["url"]
					indices = (link["indices"][0], link["indices"][1])
					sizes = link["sizes"]
					type = link["type"]
					photo_loaded.append({"id":id, "display_url":display_url, "expanded_url": expanded_url, "media_url": media_url,
						"media_url_https":media_url_https, "url":url, "indices":indices, "sizes":sizes, "type":type})
				pub.mediaTwitter.media	= photo_loaded 
		
			pub.mediaInstagram = None
			pub.mediaFacebook = None

			#print pub.post_id
			escritor.write(pub.to_JSON_one_line())
			print pub.to_JSON_one_line()
			#break



def mainInstagram(escritor):

	with open("postsInstagram.txt",'r') as f:
		lines = f.readlines()


	for line in lines:
		
		if ((line[0] == '@') or (line[0] == '#')):
			print line
			escritor.write(line);
		elif (line[0] == '{'):

			print line

			var_json	= json.loads(line)



			pub			= PostConsolidado() 
			pub.idNumber			= var_json["id"]
			pub.idString			= str(var_json["id"])
			pub.creation_date	= 	var_json["created_time"]
			pub.iso_language_code = None


			#seccion del user
			id				= var_json["user"]["id"]
			nameShort	= var_json["user"]["username"]
			nameLong			= var_json["user"]["full_name"]
			#user_url			= "https://instagram.com/%s"%(user_screen_name)	
			profile_background_image_url = None
			profile_image_url = var_json["user"]["profile_picture"]


			pub.user_owner	= {
				"id" : id, "nameLong" : nameLong, "nameShort" : nameShort, "profile_background_image_url" : profile_background_image_url,
				"profile_image_url" : profile_image_url
			}
			

			pub.network		= 2
			pub.source		= None
			pub.urlPost		= var_json["link"]
			pub.report_status = 0

			if(var_json["caption"] == None):
				pub.text = ""
			else:
				pub.text			= var_json["caption"]["text"]

			


			pub.mediaGeneral = MediaGeneral()
			



			list_hashtags		= []
			if (len(var_json["tags"]) > 0) :
				for hashtag in var_json["tags"]:
					inicio = pub.text.lower().find("#" + hashtag)
					fin = inicio + len(hashtag)
					indices	= (inicio, fin + 1)
					text	= hashtag
					list_hashtags.append({"text":text, "indices":indices})
				pub.mediaGeneral.hashtags = list_hashtags

			"""
			list_user_mentions	= []
			if (len(var_json["users_in_photo"]) > 0):
				for user_mention in var_json["users_in_photo"]:
					indices	= (-1, -1)
					text	= user_mention["user"]["username"]
					list_user_mentions.append({"screen_name":text, "indices":indices})
				pub.post_media.user_mentions = list_user_mentions
			"""
			
			"""
			list_links			= []
			if "urls" in var_json["entities"].keys() :
				for link in var_json["entities"]["urls"]:
					indices	= (link["indices"][0], link["indices"][1])
					text	= link["expanded_url"]
					list_links.append({"extended_url":text, "indices":indices})
				pub.post_media.extern_links = list_links
			"""

			"""
			if "media" in var_json["entities"].keys():
				for link in var_json["entities"]["media"]:
					indices	= (link["indices"][0], link["indices"][1])
					text	= link["expanded_url"]
					list_links.append({"extended_url":text, "indices":indices})
				pub.post_media.extern_links = list_links
			"""

			pub.mediaTwitter = None

			pub.mediaInstagram = MediaInstagram()
			pub.mediaInstagram.typeMedia = var_json["type"]

			photo_loaded		= []			
			if (len(var_json["images"]) > 0):

				resolution = 1
				url	= var_json["images"]["thumbnail"]["url"]
				width = var_json["images"]["thumbnail"]["width"]
				height = var_json["images"]["thumbnail"]["height"]
				photo_loaded.append({"resolution":resolution, "url": url, "width":width, "height": height})

				resolution = 2
				url	= var_json["images"]["low_resolution"]["url"]
				width = var_json["images"]["low_resolution"]["width"]
				height = var_json["images"]["low_resolution"]["height"]
				photo_loaded.append({"resolution":resolution, "url": url, "width":width, "height": height})

				resolution = 3
				url	= var_json["images"]["standard_resolution"]["url"]
				width = var_json["images"]["standard_resolution"]["width"]
				height = var_json["images"]["standard_resolution"]["height"]
				photo_loaded.append({"resolution":resolution, "url": url, "width":width, "height": height})

				pub.mediaInstagram.images	= photo_loaded 
		

			video_loaded		= []
			if "videos" in var_json.keys():
				
				resolution = 1
				url	= var_json["videos"]["low_bandwidth"]["url"]
				width = var_json["videos"]["low_bandwidth"]["width"]
				height = var_json["videos"]["low_bandwidth"]["height"]
				video_loaded.append({"resolution":resolution, "url": url, "width":width, "height": height})

				resolution = 2
				url	= var_json["videos"]["low_resolution"]["url"]
				width = var_json["videos"]["low_resolution"]["width"]
				height = var_json["videos"]["low_resolution"]["height"]
				video_loaded.append({"resolution":resolution, "url": url, "width":width, "height": height})

				resolution = 3
				url	= var_json["videos"]["standard_resolution"]["url"]
				width = var_json["videos"]["standard_resolution"]["width"]
				height = var_json["videos"]["standard_resolution"]["height"]
				video_loaded.append({"resolution":resolution, "url": url, "width":width, "height": height})

				pub.mediaInstagram.videos	= video_loaded 


			pub.mediaFacebook = None

			#print pub.post_id
			escritor.write(pub.to_JSON_one_line())

			print pub.to_JSON_one_line()
			#break



def mainFacebook(escritor):
	with open("postsFacebook.txt",'r') as f:
		lines = f.readlines()


	for line in lines:
		
		last = "@"

		if ((line[0] == '@') or (line[0] == '#')):
			print line
			escritor.write(line);
			last = line[0]
		elif (line[0] == '{'):

			print line

			var_json	= json.loads(line)
			#print var_json



			# No continuo si existe ["story"]
			# "shared" in ["status_type"]
			# si no existe ["link"]. en ese caso viene de twitter
			# si se subio de Twitter o Instagram

			if ("story" in var_json.keys()):
				print 'ELIMINADO'
				print "------------"
				print
				continue

			if ("status_type" in var_json.keys()):
				if ("shared" in var_json["status_type"]): #quitar si es que se desean los compartidos
					print "ELIMINADO"
					print "------------"
					print
					continue

			if not("link" in var_json.keys()):
				print "ELIMINADO"
				print "------------"
				print
				continue

			if ("application" in var_json.keys()):
				if (("Twitter" in var_json["application"]["name"]) or ("Instagram" in var_json["application"]["name"])):
					print "ELIMINADO"
					print "------------"
					print
					continue


			pub			= PostConsolidado() 
			pub.idNumber			= var_json["id"]
			pub.idString			= str(var_json["id"])
			pub.creation_date	= 	var_json["created_time"]
			pub.iso_language_code = None

	

			#seccion del user
			id				= var_json["from"]["id"]
			nameShort	= None #username no disponible
			nameLong			= var_json["from"]["name"]
			#user_url			= "https://facebook.com/%s"%(user_id)	
			profile_background_image_url = None
			profile_image_url = None

			pub.user_owner	= {
				"id" : id, "nameLong" : nameLong, "nameShort" : nameShort, "profile_background_image_url" : profile_background_image_url,
				"profile_image_url" : profile_image_url
			}
				

			pub.network = 3

			if (last == "@"):
				pub.source		= "Facebook"
			else:
				pub.source		= var_json["application"]["name"]

			pub.urlPost		= var_json["link"]

			pub.report_status = 0

			mensaje_post = ""
			if ("message" in var_json.keys()):
				if(var_json["message"] == None):
					pub.text = ""
				else:
					pub.text			= var_json["message"]
			elif ("caption" in var_json.keys()):
				if(var_json["caption"] == None):
					pub.text = ""
				else:
					pub.text			= var_json["caption"]
			else: # existen casos de videos en el que no hay texto ni nada
				pub.text = ""
			
			mensaje_post = pub.text


			pub.mediaGeneral = MediaGeneral()



			list_hashtags		= []
			for word in mensaje_post.encode('utf-8').split():
				if word.startswith('#'):
					inicio = pub.text.encode('utf-8').lower().find(word.lower())
					fin = inicio + len(word)
					indices	= (inicio, fin)
					text	= word
					list_hashtags.append({"text":text, "indices":indices})

			pub.mediaGeneral.hashtags = list_hashtags



			"""
			list_user_mentions	= []
			if ("message_tags" in var_json.keys()):
				for user_mention in var_json["message_tags"]:
					for item in var_json["message_tags"][user_mention]:
						#print item
						indices	= (item["offset"], item["offset"] + item["length"])
						text	= item["name"]
						list_user_mentions.append({"screen_name":text, "indices":indices})

			#print list_user_mentions
			pub.post_media.user_mentions = list_user_mentions
			"""

			pub.mediaFacebook = MediaFacebook()

			photo_loaded		= []			
			if ("picture" in var_json.keys()):
				url	= var_json["picture"]
				photo_loaded.append({"media_url":url})
				pub.mediaFacebook.images	= photo_loaded 



			video_loaded		= []
			if ("type" in var_json.keys()):
				if ("video" in var_json["type"]):
					url	= var_json["source"]
					video_loaded.append({"media_url":url})
					pub.mediaFacebook.videos	= video_loaded 

			pub.mediaTwitter = None
			pub.mediaInstagram = None

			#print pub.post_id
			escritor.write(pub.to_JSON_one_line())

			print pub.to_JSON_one_line()


def main():


	escritor = open("posts.txt",'w')

	mainTwitter(escritor)
	mainInstagram(escritor)
	mainFacebook(escritor)

	escritor.close()

main()