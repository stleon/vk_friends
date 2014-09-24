from glob import glob
from main import VkFriends
from settings import token, my_id, api_v, max_workers, deep
import networkx as nx
import matplotlib.pyplot as plt

def adder(node):
	if node not in g.nodes():
		g.add_node(node)


if not glob('graph'):
	if not glob('deep_friends_dct'):
		VkFriends.save_load_deep_friends('deep_friends_dct', True, VkFriends(token, my_id, api_v, max_workers).deep_friends(deep))
	
	g = nx.Graph()

	for k, v in VkFriends.save_load_deep_friends('deep_friends_dct', False).items():
		adder(k)
		if v:
			for i in v:
				adder(i)
				g.add_edge(k, i)
	VkFriends.save_load_deep_friends('graph', True, g)

g = VkFriends.save_load_deep_friends('graph', False)

print(g.number_of_nodes())
print(g.number_of_edges())

print(nx.average_clustering(g)) # коэффициент кластеризации