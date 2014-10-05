import json
from main import VkFriends
from settings import token, my_id, api_v, max_workers, delay, deep


class D3(VkFriends):
	"""
	Генерит json, дабы можно было заюзать http://bl.ocks.org/mbostock/4062045
	{
		"nodes":[
			{"name":"Myriel","group":1},
			{"name":"Napoleon","group":1},
			{"name":"Mlle.Baptistine","group":1}
		],
		"links":[
			{"source":1,"target":0,"value":1},
			{"source":2,"target":0,"value":8}
		]
	}
	target - Myriel, source 1 - Napoleon
	"""

	def __init__(self, token, my_id, api_v, max_workers):
		VkFriends.__init__(self, token, my_id, api_v, max_workers)
		self.friendships = self.common_friends()
		self.js = {"nodes": [], "links": []}
		self.write_json(self.to_json())

	def to_json(self):
		"""
		Из self.friendships сначала составляем узлы, затем ребра
		Если одновременно, то ребра вначале могут ссылаться на несуществующие узлы
		Group везде одинаковый, но добавлено photo
		"""
		for i in self.friendships:
			self.js['nodes'].append({"name": "%s %s" % (i[0]['first_name'], i[0]['last_name']),
									 												"group": 1, "photo": i[0]['photo']})
		for i in self.friendships:
			if i[1]:
				find_world = '%s %s' % (i[0]['first_name'], i[0]['last_name'])
				for d in self.js["nodes"]:
					if find_world in d.values():
						for c in i[1]:
							find_friend = '%s %s' % (c['first_name'], c['last_name'])
							for e in self.js["nodes"]:
								if find_friend in e.values():
									self.js['links'].append({"source": self.js["nodes"].index(e),
															 		"target": self.js["nodes"].index(d), "value": 1})

		return json.JSONEncoder().encode(self.js)

	def write_json(self, json):
		with open("web/miserables.json","w") as f:
			f.write(json)

if __name__ == '__main__':
	a = D3(token, my_id, api_v, max_workers)