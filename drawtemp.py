import cPickle as pk
from matplotlib import pyplot as plt
import cp
import codecs

fpath = 'results/'

topo = '30/'
servProc = 'exp/' # exp,normal,pareto
condition = 'heter/' # heterogeneous,lack,over,suitable
policy = 'greedy'
showORsave = 0 #0:show, 1:save
tkSize = 16
lgSize = 20
lbSize = 22

filename = fpath + topo + servProc + condition + policy

with codecs.open(filename+'/value', 'r') as f:
    value = cp.load(f)[0]

with codecs.open(filename+'/tp', 'r') as f:
    tp = cp.load(f)[0]

with codecs.open(filename+'/qlen', 'r') as f:
    qlen = cp.load(f)[0]

# x = filter(lambda e: e < 1001, value.keys()) #V
# x = sorted(x)
x = [i * 5 for i in range(130)]

values = [value[v] for v in x]
tps = [tp[v] for v in x]
qlens = [qlen[v] for v in x]

plt.figure(figsize=(6, 10),dpi=98)
p1 = plt.subplot(211)
p2 = plt.subplot(212)

p1.plot(x, values, '-*r')
p1.set_xlabel('V', fontsize=lbSize)
p1.set_ylabel('Communication Cost', fontsize=lbSize)

p2.plot(x, tps, '-*g')
p2.set_xlabel('V', fontsize=lbSize)
p2.set_ylabel('Throughput', fontsize=lbSize)

# plt.figure()
# plt.plot(x, qlens, '-*g')
# plt.xlabel('V')
# plt.ylabel('Average Queue Length')

if showORsave == 0:
	plt.show()
else:
	plt.savefig(filename + '/conbine.eps')
plt.close()