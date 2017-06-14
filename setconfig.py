import numpy as np
from random import randint, shuffle, choice
import networkx as nx
import cp
import codecs
from procs import procs, generate
import math
from matplotlib import pyplot as plt

'''
topo
	10: Fat-tree with parameter k.
	20: VL2 with parameter DI, DA and NH.
	30: Jellyfish with parameter k and r.
	40: small world 20 switches and 4 controllers.
	##50: F10
	60: canonical 3-tier
condition
	homo    : ns * arrRate = nc * average servRate
	heter   : ns * arrRate = nc * average servRate but heterogeneous
	over    : ns * arrRate < nc * average servRate
	lack    : ns * arrRate > nc * average servRate
'''
config = {}
topo = 10
arrProc = 'trace'

condition = 'homo'
savname = 'hotspot'

# For 10 Fat-tree
k = 24

# Vs = [i * 200000 for i in range(26)]
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

if topo == 10:  # Fat-tree
	parameter = str(k)
	numhost = int(k**3 / 4)
	numedge = int(k**2 / 2)
	numagg = int(k**2 / 2)
	numcore = int(k**2 / 4)

	nc = k // 2
	ns = int(5*(k**2) / 4)

	hosts = [x for x in range(0, numhost)]
	edges = [x for x in range(numhost, numhost + numedge)]
	aggs = [x for x in range(numhost + numedge, numhost + numedge + numagg)]
	cores = [x for x in range(numhost + numedge + numagg, ns + numhost)]

	G = nx.Graph()
	G.add_nodes_from(hosts)
	G.add_nodes_from(edges)
	G.add_nodes_from(aggs)
	G.add_nodes_from(cores)

	stride = int(k/2)
	s = 0
	e = numhost  # edge switch
	for h in hosts:  # add link between host and edge
		if s >= stride:
			s = 0
			e += 1
		G.add_edge(h, e)
		s += 1

	for e in edges:  # add link between edge and agg
		fe = e // stride * stride
		temp_aggs = [fe + (numedge) + i for i in range(stride)]
		for a in temp_aggs:
			G.add_edge(e, a)

	start = 0  # the start agg switch core link to
	s = 0
	for i in range(numcore):  # add link between agg and core
		if(s >= stride):
			s = 0
			start = start + 1
		j = start
		while j < numagg:
			G.add_edge(aggs[j], cores[i])
			j += stride
		s += 1

	controllers = [i * 2 * (k**2 // 4) for i in range(nc)]

	# controllers = [int(i * (k / 2)) for i in range(nc)]
	hops = np.zeros((ns, nc))
	for i in range(ns):
		for j in range(nc):
			hops[i,j] = nx.shortest_path_length(G, numhost + i, controllers[j])

	Xstatic = np.zeros((ns, nc+1))
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
	hotspots = [i for i in range(int(k/2))] + [int(k**2/2)+i for i in range(int(k/2))]
else:
	raise Exception('No Such Topo!')

config['parameter'] = parameter
config['hops'] = arrToLst(hops)
config['Xstatic'] = arrToLst(Xstatic)
config['ns'] = ns
config['nc'] = nc
config['hotspots'] = hotspots
config['hotarrRate'] = hotarrRate
config['arrRate'] = arrRate

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

alpha = np.sum(hops) / (0.625 * k**3)

config['u'] = [u for i in range(ns)]
config['alpha'] = [alpha for i in range(ns)]

print('alpha:', alpha)
print('u:', u)
print("ns:", ns)
print("nc:", nc)


with codecs.open('config/' + savname, 'w+', 'utf-8') as f:
	cp.dump(f, config)