from matplotlib import pyplot as plt
import cp
import codecs
import numpy as np

numofTS = 50
nc = 720
V = 40000
showORsave = 0

fpath = 'results/'
topo = '10/'
servProc = 'trace/' # exp,normal,pareto
condition = 'hotspot/'
# policy = 'greedy/' # random, JSQ, static, greedy
parameter = '24'

filename = fpath + topo + servProc + condition #+ policy #+ parameter

tkSize = 20  # 40000
lgSize = 26  # Static
lbSize = 34  # Time-slot

target = 'qlenc'
policies = ['Static', 'Random', 'JSQ', 'Greedy']

with codecs.open(filename + 'static/' + parameter + '/' + target, 'r') as f: # parameter + '/' + target, 'r') as f:
    target_static = cp.load(f)[0]
with codecs.open(filename + 'random/' + parameter + '/' + target, 'r') as f: # parameter + '/' + target, 'r') as f:
    target_random = cp.load(f)[0]
with codecs.open(filename + 'JSQ/' + parameter + '/' + target, 'r') as f: # parameter + '/' + target, 'r') as f:
    target_JSQ = cp.load(f)[0]
with codecs.open(filename + 'greedy/' + parameter + '/' + target, 'r') as f: # parameter + '/' + target, 'r') as f:
    target_greedy = cp.load(f)[0]

vars_static = [np.var(target_static[t][V]) for t in range(numofTS)]
vars_random = [np.var(target_random[t][V]) for t in range(numofTS)]
vars_JSQ = [np.var(target_JSQ[t][V]) for t in range(numofTS)]
vars_greedy = [np.var(target_greedy[t][V]) for t in range(numofTS)]

# colors = ['-or', '-ob', '-og', '-oy', '-*r', '-*b', '-*g', '-*y']
colors = ['-or', '-sb', '-dg', '-*y']
plt.figure(figsize=(11, 8))

plt.plot(list(range(numofTS)), vars_static, colors[0], list(range(numofTS)), vars_random, colors[1], \
list(range(numofTS)), vars_JSQ, colors[2], list(range(numofTS)), vars_greedy, colors[3], linewidth=2)
plt.legend(policies, loc=0, fontsize=lgSize)

plt.xlabel('Time-slot', fontsize=lbSize)
plt.ylabel('Variance of Queue Backlog($\\times 10^8$)', fontsize=lbSize)
plt.xticks([i * 10 for i in range(6)], fontsize=tkSize)
plt.yticks([-10**8, 0, 10**8, 5 * 10**8, 9 * 10**8], fontsize=tkSize)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), fontsize=tkSize)
# plt.yticks([0, 300, 600], fontsize=tkSize)
# plt.title('Queue Length of Controller(' + topo + servProc + condition + policy + ')')
# plt.legend(handles, names, loc=0, fontsize=lgSize)
if showORsave == 0:
	plt.show()
else:
	plt.savefig(filename + '/var'+ '_' + str(V) +'.eps')