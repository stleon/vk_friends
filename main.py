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
			self.friendships = list(map(lambda x: self.common_friends(self.my_id, x), self.all_friends))
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
		# удаляем деактивированные аккаунты
		return list(filter((lambda x: 'deactivated' not in x.keys()), r['items']))

	def common_friends(self, source, target):
		"""
		read https://vk.com/dev/friends.getMutual
		Принимает идентификатор источника и ифну о цели
		Возвращает в кортеже инфу о цели и список общих друзей с инфой
		"""
		r = self.checker(requests.get(self.request_url('friends.getMutual', 'source_uid=%s&target_uid=%s' %
																	(source, target['id']))).json())
		print(r)
		# return target, self.base_info(r['response']) if r['response'] else None # почувствуй разницу
		# берем инфу из уже полного списка
		return target, [id for i in r['response'] for id in self.all_friends if i == id['id']] if r['response'] else None

if __name__ == '__main__':
	a = VkFriends(token, my_id, api_v)
	print(a.my_name, a.my_last_name, a.my_id, a.photo)
	print(a.friendships)