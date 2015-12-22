1. Tabla de Post (PostPublicaciones / PostOpiniones
{
	"_id"					: "(long) mongo ID",
	"post_id"				: "(number) Id del post ",
	"post_creation_date"	: "(date) Fecha registro del post",
	"post_network"			: "(byte) red social donde se publico  (1-twitter,2-instagram,3-facebook)",
	"post_url"				: "(string) url del post en network origen",
	"post_text"				: "(string) Texto del post: (text->twitter)",

	"post_media"			:{
		"hashtags"				: [
			"indices" : ["ini","fin"], "text" : "", ...
		]
		"user_mentions"			: [
			"indices" : ["ini","fin"], "screen_name" : "", ...
		]
		"extern_links"			: [
			"indices" : ["ini","fin"], "extended_url" : "", ...
		]
		"photo_loaded"			: [ "url":"", ...]
	}
	"post_report_status" 	: "(integer) (0=SinReportar;1=Reportado;3=Verificado)"
	"post_user_owner": {
		"user_owner_id": "(number) usuario id",
		"user_owner_name": "(string) usuario nombre en pantalla",
		"user_owner_screen_name": "(string) usuario de twitter",
		"user_owner_url": "(string) link a página de usuario",
	}
}


