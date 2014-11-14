from glob import glob
from lib import save_or_load
from settings import m_friends_dct, d_friends_dct
import networkx as nx
import matplotlib.pyplot as plt
import operator
from datetime import datetime

class VkGraph():

	def __init__(self, s):
		if not glob(s['graph']):
			#if not glob(s[file])
			self.dct = save_or_load(s['file'], False)

			#print(self.calc(self.dct))

			self.graph = nx.from_dict_of_lists(self.dct)


			save_or_load(s['graph'], True, self.graph)
		else:
			self.graph = save_or_load(s['graph'], False)
	
	def draw_graph(self):
		# http://matplotlib.org/api/figure_api.html
		# http://networkx.github.io/documentation/latest/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html#networkx.drawing.nx_pylab.draw_networkx
		plt.figure(figsize=(19,19), dpi=450,)
		nx.draw(self.graph, node_size=100, cmap=True)
		plt.savefig("%s graph.png" % datetime.now().strftime('%H:%M:%S %d-%m-%Y'))

	def calc(self, dct):
		return len(dct.keys()), sum((len(i) for i in list(dct.values()) if i))

if __name__ == '__main__':
	deep_friends = VkGraph(d_friends_dct)
	print('Количество вершин:', deep_friends.graph.number_of_nodes())
	print('Количество ребер:', deep_friends.graph.number_of_edges())
	print('Связный граф?', nx.is_connected(deep_friends.graph))
	print('Диамерт графа:', nx.diameter(deep_friends.graph))
	print('Центр графа:', nx.center(deep_friends.graph))
	print('Радиус графа:', nx.radius(deep_friends.graph))
	print('Page Rank:', sorted(nx.pagerank(deep_friends.graph).items(), key=operator.itemgetter(1), reverse=True)[:5])
	print('Коэффициент кластеризации', nx.average_clustering(deep_friends.graph))
	deep_friends.draw_graph()
