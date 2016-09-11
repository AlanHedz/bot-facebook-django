from django.shortcuts import render
from django.views import generic
from pprint import pprint
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json, requests, random, re

PAGE_ACCESS_TOKEN = ""
VERIFY_TOKEN = "8332005461"
jokes = { 'hola': ["""ola k ase"""], }

def post_facebook_message(fbid, recevied_message):
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    joke_text = ''
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "La verdad es que no entiendo lo que dices :/" 

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

class FacebookBot(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == '8332005461':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error invalid token')
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					pprint(message)
					post_facebook_message(message['sender']['id'], message['message']['text'])
		return HttpResponse()
		
