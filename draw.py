from matplotlib import pyplot as plt
import cp
import codecs

fpath = 'results/'
topo = '10/'
servProc = 'trace/' # exp,normal,pareto
condition = 'hotspot/'
policy = 'greedy/' # random, JSQ, static, greedy
parameter = '24'
nc = 12
ns = 720

filename = fpath + topo + servProc + condition + policy + parameter
showORsave = 0 #0:show, 1:save
# V = 100

tkSize = 20
lgSize = 26
lbSize = 34

numofTS = 1000

with codecs.open(filename+'/q_c', 'r', 'utf-8') as f:
    Q_C = cp.load(f)[0]

with codecs.open(filename+'/q_s', 'r', 'utf-8') as f:
    Q_S = cp.load(f)[0]

with codecs.open(filename+'/comm_cost', 'r', 'utf-8') as f:
    Comm_Cost = cp.load(f)[0]

with codecs.open(filename+'/comp_cost', 'r', 'utf-8') as f:
    Comp_Cost = cp.load(f)[0]


x = filter(lambda e: e < 21000000, Q_C[0].keys())
x = sorted(x)
avg_qc = [sum([sum(Q_C[t][v])/nc for t in range(numofTS)])/numofTS for v in x]
avg_qs = [sum([sum(Q_S[t][v])/ns for t in range(numofTS)])/numofTS for v in x]
avg_comm = [sum([sum(Comm_Cost[t][v])/nc for t in range(numofTS)])/numofTS for v in x]
avg_comp = [sum([sum(Comp_Cost[t][v])/ns for t in range(numofTS)])/numofTS for v in x]

total_cost = [avg_comm[i] + avg_comp[i] for i in range(len(x))]
total_qlen = [avg_qc[i] + avg_qs[i] for i in range(len(x))]

plt.figure()
plt.plot(x, total_cost, '-or')
# plt.title('Communication Cost(' + topo + servProc + condition + policy + ')')
plt.xlabel('V', fontsize=lbSize)
plt.ylabel('Total  Cost', fontsize=lbSize)
# plt.yticks([150, 200, 250, 300], fontsize=tkSize)
if(showORsave == 0):
	plt.show()
else:
	plt.savefig(filename + '/total_cost.eps')
plt.close()
