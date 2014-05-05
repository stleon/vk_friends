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

	def __init__(self, token, my_id, api_v):
		try:
			self.token, self.my_id, self.api_v = token, my_id, api_v
			my_inf = self.base_info([self.my_id])[0]
			self.my_name, self.my_last_name, self.photo = my_inf['first_name'], my_inf['last_name'], my_inf['photo']
			self.all_friends = self.friends(self.my_id)
		except VkException as error:
			sys.exit(error)

	def request_url(self, method_name, parameters):
		"""read https://vk.com/dev/api_requests"""
		return 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}&access_token={token}'.format(
			method_name=method_name, api_v=self.api_v, parameters=parameters, token=self.token)

	def base_info(self, ids):
		"""read https://vk.com/dev/users.get"""
		r = requests.get(self.request_url('users.get', 'user_ids=%s&fields=photo' % (','.join(map(str, ids))))).json()
		if 'error' in r.keys():
			raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
		r = r['response']
		# Проверяем, если id из settings.py не деактивирован
		if 'deactivated' in r[0].keys():
			raise VkException("User deactivated")
		return r

	def friends(self, id):
		"""
		read https://vk.com/dev/friends.get
		Принимает идентификатор пользователя
		"""
		# TODO: слишком много полей для всего сразу, город и страна не нужны для нахождения общих друзей
		r = requests.get(self.request_url('friends.get',
				'user_id=%s&fields=uid,first_name,last_name,photo,country,city,sex,bdate' % id)).json()['response']
		self.count_friends = r['count']
		#r = list(filter((lambda x: 'deactivated' not in x.keys()), r['items']))
		return {item['id']: item for item in r['items']}

	def common_friends(self):
		"""
		read https://vk.com/dev/friends.getMutual and read https://vk.com/dev/execute
		Возвращает в словаре кортежи с инфой о цели и списком общих друзей с инфой
		"""
		def parts(lst, n=25):
			""" разбиваем список на части - по 25 в каждой """
			return [lst[i:i + n] for i in iter(range(0, len(lst), n))]

		result = []
		for i in parts(list(self.all_friends.keys())):
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

	def from_where_gender(self):
		"""
		Возвращает кортеж из 3х частей
		0 -  сколько всего/в% друзей в определнной локации (country, city)
		1 - список, содержащий количество друзей того или иного пола. Где индекс
			0 - пол не указан
			1 - женский;
			2 - мужской;
		2 - сколько друзей родилось в тот или иной день
		"""
		locations, all, genders, bdates = [{}, {}], [0, 0], [0, 0, 0], {}

		def calculate(dct, all):
			return {k: (dct[k], round(dct[k]/all * 100, 2)) for k, v in dct.items()}

		def constr(location, dct, ind):
			if location in dct.keys():
				place = dct[location]["title"]
				locations[ind][place] = 1 if place not in locations[ind] else locations[ind][place] + 1
				all[ind] += 1

		for i in self.all_friends.values():
			constr("country", i, 0)
			constr("city", i, 1)
			if "sex" in i.keys():
				genders[i["sex"]] += 1
			if "bdate" in i.keys():
				date = '.'.join(i["bdate"].split(".")[:2])
				bdates[date] = 1 if date not in bdates else bdates[date] + 1

		return (calculate(locations[0], all[0]), calculate(locations[1], all[1])), genders, bdates

if __name__ == '__main__':
	a = VkFriends(token, my_id, api_v)
	print(a.my_name, a.my_last_name, a.my_id, a.photo)
	print(a.common_friends())
	print(a.from_where_gender())