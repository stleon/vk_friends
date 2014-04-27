import sys
import requests
from settings import token, my_id, api_v

class VkException(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message


class VkFriends():
	"""
	Находит друзей, находит общих друзей
	"""

	@staticmethod
	def checker(r):
		if 'error' in r.keys():
			raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
		else:
			return r

	def __init__(self, token, my_id, api_v):
		try:
			self.token, self.my_id, self.api_v = token, my_id, api_v
			my_inf = self.base_info([self.my_id])[0]
			self.my_name, self.my_last_name, self.photo = my_inf['first_name'], my_inf['last_name'], my_inf['photo']
			self.all_friends = self.friends(self.my_id)
			self.friendships = self.common_friends()
		except VkException as error:
			sys.exit(error)

	def request_url(self, method_name, parameters):
		"""read https://vk.com/dev/api_requests"""
		return 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}&access_token={token}'.format(
			method_name=method_name, api_v=self.api_v, parameters=parameters, token=self.token)

	def base_info(self, ids):
		"""read https://vk.com/dev/users.get"""
		r = self.checker(requests.get(self.request_url('users.get', 'user_ids=%s&fields=photo' %
														(','.join(map(str, ids))))).json())['response']
		# Проверяем, если id из settings.py не деактивирован
		if 'deactivated' in r[0].keys():
			raise VkException("User deactivated")
		return r

	def friends(self, id):
		"""
		read https://vk.com/dev/friends.get
		Принимает идентификатор пользователя
		Возвращает список активных анкет с инфой
		"""
		r = requests.get(self.request_url('friends.get',
										  'user_id=%s&fields=uid,first_name,last_name,photo' % id)).json()['response']
		#self.count_friends = r['count']
		return {item['id']: item for item in r['items']}

	def common_friends(self):
		"""
		read https://vk.com/dev/friends.getMutual
		read https://vk.com/dev/execute
		Возвращает в кортеже инфу о цели и список общих друзей с инфой
		"""
		def f(lst, n=25):
			# разбиваем на 25 частей
			return [lst[i:i + n] for i in iter(range(0, len(lst), n))]

		result = []
		for i in f(list(self.all_friends.keys())):
			# Формируем code (параметр execute)
			code = 'return {'
			for id in i:
				code = '%s%s' % (code, '"%s": API.friends.getMutual({"source_uid":%s, "target_uid":%s}),' % (id, self.my_id, id))
			code = '%s%s' % (code, '};')

			for key, val in requests.get(self.request_url('execute', 'code=%s' % code)).json()['response'].items():
				if int(key) in list(self.all_friends.keys()):
					# берем инфу из уже полного списка
					result.append((self.all_friends[int(key)], [self.all_friends[int(i)] for i in val] if val else None))

		return result

if __name__ == '__main__':
	a = VkFriends(token, my_id, api_v)
	print(a.my_name, a.my_last_name, a.my_id, a.photo)
	print(a.friendships)