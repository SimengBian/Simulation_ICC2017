import numpy as np
from random import randint, shuffle, choice
import networkx as nx
import cp
import codecs
from procs import procs
import math
from matplotlib import pyplot as plt

config = {}
topo = 20
arrProc = 'exp'

condition = 'homo'
savname = 'hotspot'

# For 20 VL2
DI = 48  # degree of intermediate switch
DA = 48  # degree of aggregate switch
NH = 2  # number of hosts of one TOR switch

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

if topo == 20: #VL2
	parameter = str(DI) + '_' + str(DA) + '_' + str(NH)

	numhost = int(NH * (DI*DA/4))
	numToR = int(DI*DA/4)
	numagg = DI
	numinter = int(DA / 2)

	ns = numToR + numagg + numinter
	nc = int(DA / 4) # every two pod

	hosts = [x for x in range(0, numhost)]
	ToRs = [x for x in range(numhost, numhost + numToR)]
	aggs = [x for x in range(numhost + numToR, numhost + numToR + numagg)]
	inters = [x for x in range(numhost + numToR + numagg, ns + numhost)]

	G = nx.Graph()
	G.add_nodes_from(hosts)
	G.add_nodes_from(ToRs)
	G.add_nodes_from(aggs)
	G.add_nodes_from(inters)

	for i in inters:  # add links between intermediate and aggregate
		for a in aggs:
			G.add_edge(i,a)

	i = 0
	while i < numagg:  # add links between aggregate and ToR
		a1 = aggs[i]
		a2 = aggs[i+1]
		subToRs = [ToRs[j] for j in range(i//2 * int(DA/2), (i//2+1) * int(DA/2))]
		for t in subToRs:
			G.add_edge(a1, t)
			G.add_edge(a2, t)
		i += 2

	for h in hosts:  # add links between ToR and host
		G.add_edge(h, ToRs[h//NH])

	controllers = [i * (DA * NH) for i in range(nc)]
	# controllers = [0, 2, 8, 12]
	print(controllers)
	# hops = np.zeros((ns, nc))
	# for i in range(ns):
	# 	s = numhost + i
	# 	for j in range(nc):
	# 		c = controllers[j]
	# 		if s in ToRs:
	# 			if G.has_edge(s, c): hops[i, j] = 1
	# 			else: hops[i, j] = 5
	# 		elif s in aggs:
	# 			if G.has_edge(s, 2*c//int(DA/2) + numhost): hops[i, j] = 2
	# 			else: hops[i, j] = 4
	# 		elif s in inters:
	# 			hops[i, j] = 3

	hops = np.zeros((ns, nc))
	for i in range(ns):
		for j in range(nc):
			hops[i,j] = nx.shortest_path_length(G, numhost + i, controllers[j])

	Xstatic = np.zeros((ns, nc+1))
	ci = 0  # Round-Robin for intermedia switch
	ca = 0  # Round-Robin for aggregate switch
	ct = 0  # Round-Robin for ToR switch
	for i in range(ns):
		l = list(hops[i])
		minhop = min(l)
		if l.count(minhop) == 1:
			j = l.index(minhop)
			Xstatic[i, j] = 1
		else:  # has more than one minimum hop
			if numhost + i in ToRs:
				Xstatic[i, ct] = 1
				ct += 1
				ct = ct % nc
			elif numhost + i in aggs:
				Xstatic[i, ca] = 1
				ca += 1
				ca = ca % nc
			elif numhost + i in inters:
				Xstatic[i, ci] = 1
				ci += 1
				ci = ci % nc

	hotspots = [i for i in range(DA // 2)] + [numToR + 1, numToR + 2]
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


alpha = np.sum(hops) / (ns * nc)
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