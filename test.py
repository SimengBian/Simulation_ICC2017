from matplotlib import pyplot as plt
import cp
import codecs

fpath = 'results/'
topo = '10/'
servProc = 'exp/' # exp,normal,pareto
condition = 'hotspot/'
policy = 'greedy/' # random, JSQ, static, greedy
parameter = '24'

showORsave = 0
Vs = [i * 1000000 for i in range(31)]

filename = fpath + topo + servProc + condition + policy + parameter
V = 5000000

tkSize = 20
lgSize = 26
lbSize = 34

numofTS = 10000

with codecs.open(filename + '/avg_qc', 'r+', 'utf-8') as f:
    avg_qc = cp.load(f)[0] # avg_qc)

with codecs.open(filename + '/avg_qs', 'r+', 'utf-8') as f:
    avg_qs = cp.load(f)[0] # avg_qs)

with codecs.open(filename + '/avg_comm', 'r+', 'utf-8') as f:
    avg_comm = cp.load(f)[0] # avg_comm)

with codecs.open(filename + '/avg_comp', 'r+', 'utf-8') as f:
    avg_comp = cp.load(f)[0] # avg_comp)

with codecs.open(filename + '/total_cost', 'r+', 'utf-8') as f:
    total_cost = cp.load(f)[0] # total_cost)

with codecs.open(filename + '/total_qlen', 'r+', 'utf-8') as f:
    total_qlen = cp.load(f)[0] # total_cost)

with codecs.open(filename + '/Q_C_0', 'r+', 'utf-8') as f:
    Q_C_0 = cp.load(f)[0] # Q_C_0)

with codecs.open(filename + '/Q_C_1', 'r+', 'utf-8') as f:
    Q_C_1 = cp.load(f)[0] # Q_C_1)

with codecs.open(filename + '/Q_S_0', 'r+', 'utf-8') as f:
    Q_S_0 = cp.load(f)[0] # Q_S_0)

if topo == '10/':
    with codecs.open(filename + '/Q_S_12', 'r+', 'utf-8') as f:
        Q_S_12 = cp.load(f)[0] # Q_S_12)

    with codecs.open(filename + '/Q_S_24', 'r+', 'utf-8') as f:
        Q_S_24 = cp.load(f)[0] # Q_S_24)

if topo == '60/':
    with codecs.open(filename + '/Q_S_25', 'r+', 'utf-8') as f:
        Q_S_25 = cp.load(f)[0] # Q_S_25)

    with codecs.open(filename + '/Q_S_50', 'r+', 'utf-8') as f:
        Q_S_50 = cp.load(f)[0] # Q_S_50)



x = [10*i for i in range(1000)]

plt.figure(figsize=(11, 8))
y = [Q_S_24[V][i] for i in x]
plt.plot(x, y, '-or')
plt.xlabel('Time slot', fontsize=lbSize)

# plt.ylabel('Queue Backlog', fontsize=lbSize)
plt.ylabel('Queue Backlog($\\times 10^7$)', fontsize=lbSize)

plt.xticks([0, 2500, 5000, 7500, 10000], fontsize=tkSize)
# plt.yticks([3e6, 6e6, 9e6, 12e6], fontsize=tkSize)
plt.yticks([3000000*z for z in range(1, 5)], fontsize=tkSize)

# plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0), fontsize=tkSize)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), fontsize=tkSize)

if showORsave == 0:
    plt.show()
else:
    plt.savefig(filename + '/S0.svg', format="svg", dpi=1200)

