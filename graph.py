from glob import glob
from main import VkFriends
from settings import token, my_id, api_v, max_workers
import networkx as nx


if not glob('deep_friends_dct'):
	VkFriends.save_load_deep_friends('deep_friends_dct', True, VkFriends(token, my_id, api_v, max_workers).deep_friends(1))

g = nx.Graph()

def adder(node):
	if node not in g.nodes():
		g.add_node(node)

for k, v in VkFriends.save_load_deep_friends('deep_friends_dct', False).items():
	adder(k)
	for i in v:
		adder(i)
		g.add_edge(k, i)