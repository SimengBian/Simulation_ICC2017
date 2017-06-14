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

numofTS = 7000
filename = fpath + topo + servProc + condition + policy + parameter

with codecs.open(filename+'/q_s', 'r', 'utf-8') as f:
    Q_S = cp.load(f)[0]

x = filter(lambda e: e < 21000000, Q_S[1].keys())
x = sorted(x)
avg_qc = [sum([sum(Q_S[t][v])/ns for t in range(1, numofTS)])/numofTS for v in x]

with codecs.open(filename+'/avg_qs', 'w+', 'utf-8') as f:
    cp.dump(f, avg_qs)