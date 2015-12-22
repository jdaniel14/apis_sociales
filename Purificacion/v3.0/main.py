
import json

import simplejson as json2

import pprint

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



def mainTwitter(escritor):

	with open("postsTwitter.txt",'r') as f:
		lines = f.readlines()



	for line in lines:
		
		if ((line[0] == '@') or (line[0] == '#')):
			print line
			#escritor.write(line);
		elif (line[0] == '{'):


			var_json	= json.loads(line)

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

			pub			= Post() 
			pub.post_id				= var_json["id"]
			pub.post_creation_date	= var_json["created_at"]
			pub.post_network		= var_json["source"]
			pub.post_text			= var_json["text"]

			#seccion del user
			user_id				= var_json["user"]["id"]
			user_screen_name	= var_json["user"]["screen_name"]
			user_name			= var_json["user"]["name"]
			user_url			= "https://twitter.com/%s"%(user_screen_name)	
			pub.post_user_owner	= {
				"user_owner_id" : user_id, "user_owner_name" : user_name, "user_owner_screen_name" : user_screen_name, "user_owner_url" : user_url
			}
				
			pub.post_url		= "https://twitter.com/%s/status/%s"%(user_screen_name, pub.post_id)
			
			print pub.post_id
			print pub.post_url

			list_hashtags		= []
			if "hashtags" in var_json["entities"].keys() :
				for hashtag in var_json["entities"]["hashtags"]:
					indices	= (hashtag["indices"][0], hashtag["indices"][1])
					text	= hashtag["text"]
					list_hashtags.append({"text":text, "indices":indices})
				pub.post_media.hashtags = list_hashtags

			list_user_mentions	= []
			if "user_mentions" in var_json["entities"].keys() :
				for user_mention in var_json["entities"]["user_mentions"]:
					indices	= (user_mention["indices"][0], user_mention["indices"][1])
					text	= user_mention["screen_name"]
					list_user_mentions.append({"screen_name":text, "indices":indices})
				pub.post_media.user_mentions = list_user_mentions

			list_links			= []
			if "urls" in var_json["entities"].keys() :
				for link in var_json["entities"]["urls"]:
					indices	= (link["indices"][0], link["indices"][1])
					text	= link["expanded_url"]
					list_links.append({"extended_url":text, "indices":indices})
				pub.post_media.extern_links = list_links

			if "media" in var_json["entities"].keys():
				for link in var_json["entities"]["media"]:
					indices	= (link["indices"][0], link["indices"][1])
					text	= link["expanded_url"]
					list_links.append({"extended_url":text, "indices":indices})
				pub.post_media.extern_links = list_links

			photo_loaded		= []
			
			#if "media" in var_json["entities"].keys():
			if "extended_entities" in var_json:
			#	for link in var_json["entities"]["media"]:
				for link in var_json["extended_entities"]["media"]:
					text	= link["media_url"]
					photo_loaded.append({"media_url":text})
				pub.post_media.photo_loaded	= photo_loaded 
		
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



			pub			= Post() 
			pub.post_id				= var_json["id"]
			pub.post_creation_date	= var_json["created_time"]
			pub.post_network		= "Instagram"
			if(var_json["caption"] == None):
				pub.post_text = ""
			else:
				pub.post_text			= var_json["caption"]["text"]

			#seccion del user
			user_id				= var_json["user"]["id"]
			user_screen_name	= var_json["user"]["username"]
			user_name			= var_json["user"]["full_name"]
			user_url			= "https://instagram.com/%s"%(user_screen_name)	
			pub.post_user_owner	= {
				"user_owner_id" : user_id, "user_owner_name" : user_name, "user_owner_screen_name" : user_screen_name, "user_owner_url" : user_url
			}
				
			pub.post_url		= var_json["link"]
		




			list_hashtags		= []
			if (len(var_json["tags"]) > 0) :
				for hashtag in var_json["tags"]:
					inicio = pub.post_text.lower().find("#" + hashtag)
					fin = inicio + len(hashtag)
					indices	= (inicio, fin + 1)
					text	= hashtag
					list_hashtags.append({"text":text, "indices":indices})
				pub.post_media.hashtags = list_hashtags

			list_user_mentions	= []
			if (len(var_json["users_in_photo"]) > 0):
				for user_mention in var_json["users_in_photo"]:
					indices	= (-1, -1)
					text	= user_mention["user"]["username"]
					list_user_mentions.append({"screen_name":text, "indices":indices})
				pub.post_media.user_mentions = list_user_mentions

			
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

			photo_loaded		= []			
			if (len(var_json["images"]) > 0):
				text	= var_json["images"]["standard_resolution"]["url"]
				photo_loaded.append({"media_url":text})
				pub.post_media.photo_loaded	= photo_loaded 
		

			video_loaded		= []
			if "videos" in var_json.keys():
				text	= var_json["videos"]["standard_resolution"]["url"]
				video_loaded.append({"media_url":text})
				pub.post_media.video_loaded	= video_loaded 

			#print pub.post_id
			escritor.write(pub.to_JSON_one_line())

			print pub.to_JSON_one_line()
			#break






def main():


	escritor = open("posts.txt",'w')

	mainTwitter(escritor)
	mainInstagram(escritor)

	escritor.close()

main()