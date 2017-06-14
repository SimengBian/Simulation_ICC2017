from matplotlib import pyplot as plt
import cp
import codecs

fpath = 'results/'

# topo = '10/'
arrProc = 'trace/'  # exp,normal,pareto
condition = 'hotspot/'  # heter,lack,over,homo
# parameter = '24'

target = 'total_cost'  # value tp qlen qlenvar

filename10 = fpath + '10/' + arrProc + condition
filename60 = fpath + '60/' + arrProc + condition

filename_poisson = fpath + '10/' + 'exp/' + condition
filename_pareto = fpath + '10/' + 'pareto/' + condition
# print(filename)

showORsave = 0  # 0:show, 1:save
# numofTS = 50
# V = 10


tkSize = 20  # 40000
lgSize = 26  # Static
lbSize = 34  # Communication cost

arrProcs = ['Poisson', 'Pareto'] # ['Static', 'Random', 'JSQ', 'Greedy']

# with codecs.open(filename10 + 'greedy/' + '24/' + target, 'r') as f:
with codecs.open(filename_poisson + 'greedy/' + '24/' + target, 'r') as f:
    target10= cp.load(f)[0]

# with codecs.open(filename60 + 'greedy/' + '26/' + target, 'r') as f:
with codecs.open(filename_pareto + 'greedy/' + '24/' + target, 'r') as f:
    target60= cp.load(f)[0]

x = [i * 1000000 for i in range(31)]

targets = {}

yname = ''
if target == 'total_cost':
    yname = 'Total Cost ($\\times 10^4$)'
elif target == 'total_qlen':
    yname = 'Total Queue Backlog($\\times 10^7$)'

plt.figure(figsize=(11, 8))
handles = []
names = []

colors = ['-or', '-sb', '-dg', '-*y']
plt.xlim(1000000, 30000000)

h, = plt.plot(x[1:], target10[1:], colors[0], linewidth=2)
handles.append(h)
names.append(arrProcs[0])
plt.hold(True)

h, = plt.plot(x[1:], target60[1:], colors[1], linewidth=2)
handles.append(h)
names.append(arrProcs[1])

plt.legend(arrProcs, loc=0, fontsize=lgSize)
plt.xlabel('V ($\\times 10^7$)', fontsize=lbSize)
plt.ylabel(yname, fontsize=lbSize)

plt.xticks([7500000*k for k in range(1, 5)], fontsize=tkSize)

# # For cost
# if target == 'total_cost':
#     plt.yticks([28000, 32000, 36000, 40000, 44000], fontsize=tkSize)
# # For qlen
# elif target == 'total_qlen':
#     plt.yticks([15e6, 20e6, 25e6, 30e6, 35e6], fontsize=tkSize)

'''
For exp and pareto
'''
# For cost
if target == 'total_cost':
    plt.yticks([250e2, 275e2, 300e2, 325e2, 350e2], fontsize=tkSize)
# For qlen
elif target == 'total_qlen':
    plt.yticks([15e6, 17.5e6, 20e6, 22.5e6, 25e6], fontsize=tkSize)


plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0), fontsize=tkSize)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), fontsize=tkSize)
# plt.legend(handles, names, loc=0, fontsize=lgSize)
if showORsave == 0:
    plt.show()
else:
    plt.savefig('results/10/' + target + '.svg', format="svg", dpi=1200)

plt.close()