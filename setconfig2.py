import numpy as np
from random import randint, shuffle, choice
import networkx as nx
import cp
import codecs
from procs import procs
import math
from matplotlib import pyplot as plt

'''
topo
	60: canonical 3-tier
'''
config = {}
topo = 60
arrProc = 'trace'

condition = 'homo'
savname = 'hotspot'

# For 3-tire
k3 = 26

# Vs = [i * 200000 for i in range(51)]
Vs = [i * 1000000 for i in range(31)]

hotarrRate = 200
arrRate = 5.85
svRate = 600
u = 0.6


config['Vs'] = Vs
config['topo'] = topo
config['arrProc'] = arrProc
config['condition'] = condition
parameter = ''

def arrToLst(arr):
	return [sublst for sublst in arr]

if topo == 60:
	ns = k3 ** 2 + k3
	nc = k3 // 2
	parameter = str(k3)

	ToRs = list(range(0, k3*(k3-1)))
	aggs = list(range(k3*(k3-1), k3*(k3-1) + k3))
	cores = list(range(k3*(k3-1) + k3, k3*(k3-1) + 2 * k3))

	G = nx.Graph()
	G.add_nodes_from(ToRs)
	G.add_nodes_from(aggs)
	G.add_nodes_from(cores)

	count = 0
	for a in aggs:  # add links between intermediate and aggregate
		for c in cores:
			G.add_edge(a, c)
		for j in range(k3-1):
			G.add_edge(a, ToRs[count + j])

		count += k3 - 1

	controllers = [i * 2 * (k3-1) for i in range(nc)]
	G.add_edges_from([(controllers[i], controllers[i]+ns) for i in range(nc)])
	hops = np.zeros((ns, nc))
	for i in range(ns):
		for j in range(nc):
			hops[i, j] = nx.shortest_path_length(G, i, controllers[j] + ns)
	# print(count, k3 ** 2)
	Xstatic = np.zeros((ns, nc))
	c = 0  # For Round-Robin
	for i in range(ns):
		l = list(hops[i])
		minhop = min(l)
		if l.count(minhop) == 1:
			j = l.index(minhop)
			Xstatic[i, j] = 1
		else:  # has more than one minimum hop
			Xstatic[i, c] = 1
			c += 1
			c %= nc
	hotspots = [i for i in range(k3-1)] + [k3 * (k3-1)]
else:
	raise Exception('No Such Topo!')

config['parameter'] = parameter
config['hops'] = arrToLst(hops)
config['Xstatic'] = arrToLst(Xstatic)
config['ns'] = ns
config['nc'] = nc


servRate = []
if condition == 'homo':
	servRate = [svRate for i in range(nc)]

if condition == 'heter':
	t = nc // 2
	for i in range(1, t+1):
		servRate.insert(0, svRate - i*5)
		servRate.append(svRate + i*5)

config['arrRate'] = arrRate
config['servRate'] = servRate


alpha = np.sum(hops) / (0.5*k3*(k3+1)*k3)
config['u'] = [u for i in range(ns)]
config['alpha'] = [alpha for i in range(ns)]
config['hotspots'] = hotspots
config['hotarrRate'] = hotarrRate
config['arrRate'] = arrRate

print('alpha:', alpha)
print('u:', u)
print("ns:", ns)
print("nc:", nc)


with codecs.open('config/' + savname, 'w+', 'utf-8') as f:
	cp.dump(f, config)