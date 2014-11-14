from tasks import mutual_friends, deep_friends
from celery import group
from settings import my_id, deep, m_friends_dct, d_friends_dct
from lib import request_url, friends, parts, save_or_load

def cleaner(dct):
	"""
	удаляем все заблокированные или удаленные анкеты
	"""
	return {k:v for k, v in dct.items() if v != None}

def getMutual():
	all_friends = friends(my_id)
	c_friends = group(mutual_friends.s(i) for i in parts(list(all_friends[0].keys()), 75))().get()
	result = {k: v for d in c_friends for k, v in d.items()}
	return cleaner(result)

def getDeep():
	result = {}
	for i in range(deep):
		if result:
			# те айди, которых нет в ключах + не берем id:None
			lst = list(set([item for sublist in result.values() if sublist for item in sublist]) - set(result.keys()))
			d_friends = group(deep_friends.s(i) for i in parts(list(lst), 75))().get()
			result = {k: v for d in d_friends for k, v in d.items()}
			result.update(result)
		else:
			all_friends = friends(my_id)
			d_friends = group(deep_friends.s(i) for i in parts(list(all_friends[0].keys()), 75) )().get()
			result = {k: v for d in d_friends for k, v in d.items()}
			result.update(result)

	return cleaner(result)

if __name__ == '__main__':

	if int(input('1 - mutual friends, 2 - deep friends\n')) == 1:
		save_or_load(m_friends_dct['file'], True, getMutual())
		print(save_or_load(m_friends_dct['file'], False))
	else:
		save_or_load(d_friends_dct['file'], True, getDeep())
		print(save_or_load(d_friends_dct['file'], False))
	