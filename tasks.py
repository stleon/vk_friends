from celery import Celery
from celery_app import app
import requests
from settings import my_id
from lib import request_url, make_targets, parts

@app.task
def mutual_friends(lst):
	"""
	read https://vk.com/dev/friends.getMutual and read https://vk.com/dev/execute
	"""
	result = {}
	for i in list(parts(lst, 25)):
		r = requests.get(request_url('execute.getMutual', 'source=%s&targets=%s' % (my_id, make_targets(i)), access_token=True)).json()['response']	
		for x, vk_id in enumerate(i):
			result[vk_id] = tuple(i for i in r[x]) if r[x] else None
	return result

@app.task
def deep_friends(friends):
	result = {}
	for i in list(parts(friends, 25)):
		r = requests.get(request_url('execute.deepFriends', 'targets=%s' % make_targets(i), access_token=True)).json()["response"]
	
		for x, vk_id in enumerate(i):
			result[vk_id] = tuple(r[x]["items"]) if r[x] else None

	return result