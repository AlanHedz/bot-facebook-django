from django.conf.urls import include, url
from views import FacebookBot

urlpatterns = [
	url(r'^13238c9573a9d69946999b259ec984143d83f01fc6f5d7fe2d/?$', FacebookBot.as_view())
]