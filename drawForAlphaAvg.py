from matplotlib import pyplot as plt
import cp
import codecs

fpath = 'results/'

topo = '10/'
arrProc = 'trace/'  # exp,normal,pareto
condition = 'hotspot/'  # heter,lack,over,homo
parameter = '24'

target = 'total_cost'  # value tp qlen qlenvar

filename = fpath + topo + arrProc + condition
print(filename)

showORsave = 0  # 0:show, 1:save
# numofTS = 50
# V = 10


tkSize = 20  # 40000
lgSize = 26  # Static
lbSize = 34  # Communication cost

policies = ['Greedy', 'Static', 'Random', 'JSQ']

with codecs.open(filename + 'greedy/' + parameter + '/' + target, 'r') as f:
    target_greedy = cp.load(f)[0]
value_greedy = target_greedy[1:]

with codecs.open(filename + 'static/' + parameter + '/' + 'value', 'r') as f:
    target_static = cp.load(f)[0]
value_static = [target_static[0] for i in xrange(1, 31)]

with codecs.open(filename + 'random/' + parameter + '/' + 'value', 'r') as f:
    target_random = cp.load(f)[0]
value_random = [target_random[0] for i in xrange(1, 31)]

with codecs.open(filename + 'JSQ/' + parameter + '/' + 'value', 'r') as f:
    target_JSQ = cp.load(f)[0]
value_JSQ = [target_JSQ[0] for i in xrange(1, 31)]


x = [i * 1000000 for i in xrange(1, 31)]

targets = {}

yname = 'Communication Cost ($\\times 10^4$)'
# if target == 'total_cost':
#     yname = 'Communication Cost ($\\times 10^4$)'
# elif target == 'total_qlen':
#     yname = 'Total Queue Backlog($\\times 10^7$)'

plt.figure(figsize=(11, 8))
handles = []
names = []

colors = ['-or', '-sb', '-dg', '-*y']


h, = plt.plot(x, value_greedy, colors[0], linewidth=2)
handles.append(h)
names.append(policies[0])
plt.hold(True)

h, = plt.plot(x, value_static, colors[1], linewidth=2)
handles.append(h)
names.append(policies[1])
plt.hold(True)

h, = plt.plot(x, value_random, colors[2], linewidth=2)
handles.append(h)
names.append(policies[2])
plt.hold(True)

h, = plt.plot(x, value_JSQ, colors[3], linewidth=2)
handles.append(h)
names.append(policies[3])
# plt.hold(True)

plt.legend(handles, names, loc=0, fontsize=lgSize)
plt.xlabel('V ($\\times 10^7$)', fontsize=lbSize)
plt.ylabel(yname, fontsize=lbSize)

plt.xticks([4000000*k for k in range(1, 6)], fontsize=tkSize)

# For cost
if target == 'total_cost':
    plt.yticks([28000, 34000, 40000, 46000, 50000], fontsize=tkSize)
# For qlen
elif target == 'total_qlen':
    plt.yticks([15e6, 20e6, 25e6, 30e6, 35e6], fontsize=tkSize)

'''
For exp and pareto
'''
# # For cost
# if target == 'total_cost':
#     plt.yticks([250e2, 275e2, 300e2, 325e2, 350e2], fontsize=tkSize)
# # For qlen
# elif target == 'total_qlen':
#     plt.yticks([15e6, 17.5e6, 20e6, 22.5e6, 25e6], fontsize=tkSize)


plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0), fontsize=tkSize)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), fontsize=tkSize)

if showORsave == 0:
    plt.show()
else:
    plt.savefig(filename + target + '_' + parameter +'.svg', format="svg", dpi=1200)

plt.close()