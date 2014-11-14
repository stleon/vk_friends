import requests
import random
from settings import token, api_v
import pickle

def request_url(method_name, parameters, access_token=False):
	"""read https://vk.com/dev/api_requests"""

	req_url = 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}'.format(
		method_name=method_name, api_v=api_v, parameters=parameters)

	if access_token:
		req_url = '{}&access_token={token}'.format(req_url, token=random.choice(token))

	return req_url

def friends(id):
	"""
	read https://vk.com/dev/friends.get
	Принимает идентификатор пользователя
	"""

	r = requests.get(request_url('friends.get',
		'user_id=%s&fields=uid' % id)).json()['response'] # 'hidden': 1
	# удаляем деактивированные анкеты
	r["items"] = list(filter((lambda x: 'deactivated' not in x.keys()), r['items']))
	return {item['id']: item for item in r['items']}, r['count']

def save_or_load(myfile, sv, smth=None):
	if sv and smth:
		pickle.dump(smth, open(myfile, "wb"))
	else:
		return pickle.load(open(myfile, "rb"))

parts = lambda lst, n: (lst[i:i + n] for i in iter(range(0, len(lst), n)))

make_targets = lambda lst: ",".join(str(x) for x in lst)

