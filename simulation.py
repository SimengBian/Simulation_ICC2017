from procs import procs
import numpy as np
import random
from random import shuffle
import sys
import cp
import codecs
import time
from procs import generate

from procs import procs

start = time.time()
MAX = sys.maxsize * 999999999


condition = 'hotspot'
policy = 'greedy'
configName = 'hotspot'

def lstToArr(lst):
    return np.array(lst)
with codecs.open('config/' + configName, 'r', 'utf-8') as f:
    config = cp.load(f)

parameter = config[0]['parameter']
topo = config[0]['topo']
arrProc = config[0]['arrProc']
ns = config[0]['ns']
nc = config[0]['nc']
Vs = config[0]['Vs']

hotspots = config[0]['hotspots']
hotarrRate = config[0]['hotarrRate']
arrRate    = config[0]['arrRate']

servRate = config[0]['servRate']
hops = lstToArr(config[0]['hops'])
Xstatic = lstToArr(config[0]['Xstatic'])
alpha = config[0]['alpha']
u = config[0]['u']


filename = 'results/' + str(topo) + '/' + arrProc + '/' + condition + '/' + policy + '/' + parameter

print('policy:', policy)
print('topo:', topo)
print('ns:', ns)
print('nc:', nc)
print('arrProc:', arrProc)
print('alpha:', alpha[0])
print('u:', u[0])

lastServTimes = {c: -1 for c in range(nc)}


def serve(c, servProc, servRate):
    lastServTimes[c] = -1
    q = servRate
    total = 1
    count = 0

    if lastServTimes[c] > 0:
        if lastServTimes[c] > total:
            lastServTimes[c] -= total
            total = -1
            return count
        else:
            total -= lastServTimes[c]
            count += 1
            lastServTimes[c] = -1

    while total > 0:
        lastServTimes[c] = servProc(q)
        if lastServTimes[c] > total:
            lastServTimes[c] -= total
            total = -1
            return count
        else:
            total -= lastServTimes[c]
            count += 1
            lastServTimes[c] = -1

    return count

def copy_dict(original):
    return {key: original[key] + [] for key in original.keys()}


Q_C_current = {V: [0 for c in range(nc)] for V in Vs}
Q_C_last = {V: [0 for c in range(nc)] for V in Vs}
Q_S_current = {V: [0 for s in range(ns)] for V in Vs}
Q_S_last = {V: [0 for s in range(ns)] for V in Vs}

Q_C_0 = {V:[] for V in Vs}
Q_C_1 = {V:[] for V in Vs}
Q_S_0 = {V:[] for V in Vs}

# for 3-tiered
Q_S_25 = {V:[] for V in Vs}
Q_S_50 = {V:[] for V in Vs}

# for fat-tree
Q_S_12 = {V:[] for V in Vs}
Q_S_24 = {V:[] for V in Vs}

Comm_Cost_current = {V: [0 for c in range(nc)] for V in Vs}
# Comm_Cost_last = {V: [0 for c in range(nc)] for V in Vs}
Comp_Cost_current = {V: [0 for s in range(ns)] for V in Vs}
# Comp_Cost_last = {V: [0 for s in range(ns)] for V in Vs}

total_cost_last_ts = {V: 0 for V in Vs}
error = 1e-6
T = 1
MIN_TS = 10000
blackLst = []

avg_qc = {V: 0 for V in Vs}
avg_qs = {V: 0 for V in Vs}
avg_comm = {V: 0 for V in Vs}
avg_comp = {V: 0 for V in Vs}

interested_Vs = [5000000]

while True:
    T = T + 1
    print('Time-slot:', T, 'rest:', len(Vs) - len(blackLst))
    if len(blackLst) == len(Vs) and T > MIN_TS:
        break

    # Q_C[T] = {V: [0 for c in range(nc)] for V in Vs}
    # Q_S[T] = {V: [0 for s in range(ns)] for V in Vs}
    # Comm_Cost[T] = {V: [0 for c in range(nc)] for V in Vs}
    # Comp_Cost[T] = {V: [0 for s in range(ns)] for V in Vs}

    As_now = [generate(ns, k, procs[arrProc], arrRate) for k in range(ns)]
    for hs in hotspots:
        As_now[hs] = hotarrRate

    services = [serve(k, procs['constant'], servRate[k]) for k in range(nc)]

    for V in Vs:
        X = np.zeros((ns, nc+1))
        if policy == 'greedy':
            vq = {}
            for c in range(nc):
                vq[c] = Q_C_last[V][c]

            rang = list(range(ns))
            shuffle(rang)

            for i in rang:
                rangc = list(range(nc+1))
                shuffle(rangc)
                j_opt = 0
                val_min = V * hops[i][0] + Q_C_last[V][0]
                for j in range(nc+1):
                    if j == nc:
                        val = V * alpha[i] + Q_S_last[V][i]
                    else:
                        val = V * hops[i][j] + vq[j]
                    if val < val_min:
                        val_min = val
                        j_opt = j
                X[i, j_opt] = 1
                if j_opt != nc:
                    vq[j_opt] += As_now[i]


        elif policy == 'random':
            rang = list(range(ns))
            shuffle(rang)
            for i in rang:
                j = random.randint(0, nc)
                X[i, j] = 1
        elif policy == 'JSQ':
            rang = list(range(ns))
            shuffle(rang)
            tempq = {}
            for c in range(nc):
                tempq[c] = Q_C_last[V][c]
            for i in rang:
                j = min(list(tempq.items()) + [(nc, Q_S_last[V][i])], key=lambda e: e[1])[0]
                X[i, j] = 1
                if j != nc:
                    tempq[j] += As_now[i]

        elif policy == 'static':
            X = Xstatic

        # upload to controllers
        for j in range(nc):
            Q_C_current[V][j] += Q_C_last[V][j]
            for i in range(ns):
                if X[i, j] == 1:
                    Q_C_current[V][j] += As_now[i]

        # upload to switches
        for i in range(ns):
            Q_S_current[V][i] += Q_S_last[V][i]
            if X[i, nc] == 1:
                Q_S_current[V][i] += As_now[i]

        # serve
        for j in range(nc):
            actualservicec = min(services[j], Q_C_current[V][j])
            Q_C_current[V][j] -= actualservicec
        for i in range(ns):
            actualservices = min(u[i], Q_S_current[V][i])
            Q_S_current[V][i] -= actualservices

        # Calculate communication cost
        for j in range(nc):
            tem_cost = 0
            for i in range(ns):
                tem_cost += As_now[i] * X[i, j] * hops[i, j]
            Comm_Cost_current[V][j] = tem_cost

        # Calculate computation cost
        for i in range(ns):
            if X[i][nc] == 1:
                Comp_Cost_current[V][i] = As_now[i] * alpha[i]

        gap = abs((total_cost_last_ts[V] - (T - 1) * (sum(Comm_Cost_current[V]) + sum(Comp_Cost_current[V]))) / \
                  ((total_cost_last_ts[V] + sum(Comm_Cost_current[V]) + sum(Comp_Cost_current[V])) * (T - 1)))

        if V not in blackLst and gap < error:
            blackLst.append(V)

        total_cost_last_ts[V] += sum(Comm_Cost_current[V]) + sum(Comp_Cost_current[V])

        avg_qc[V] += sum(Q_C_current[V])
        avg_qs[V] += sum(Q_S_current[V])
        avg_comm[V] += sum(Comm_Cost_current[V])
        avg_comp[V] += sum(Comp_Cost_current[V])

        if topo == 60 and V in interested_Vs:
            Q_C_0[V].append(Q_C_current[V][0])
            Q_C_1[V].append(Q_C_current[V][1])
            Q_S_0[V].append(Q_S_current[V][0])
            Q_S_25[V].append(Q_S_current[V][25])
            Q_S_50[V].append(Q_S_current[V][50])

        if topo == 10 and V in interested_Vs:
            Q_C_0[V].append(Q_C_current[V][0])
            Q_C_1[V].append(Q_C_current[V][1])
            Q_S_0[V].append(Q_S_current[V][0])
            Q_S_12[V].append(Q_S_current[V][12])
            Q_S_24[V].append(Q_S_current[V][24])

    Q_C_last = copy_dict(Q_C_current)
    Q_S_last = copy_dict(Q_S_current)
    # Comm_Cost_last = copy_dict(Comm_Cost_current)
    # Comp_Cost_last = copy_dict(Comp_Cost_current)


    Q_C_current = {V: [0 for c in range(nc)] for V in Vs}
    Q_S_current = {V: [0 for s in range(ns)] for V in Vs}
    Comm_Cost_current = {V: [0 for c in range(nc)] for V in Vs}
    Comp_Cost_current = {V: [0 for s in range(ns)] for V in Vs}


print(filename)

scores = {V: float(T) for V in Vs}
total_qlen = {V: (avg_qc[V] + avg_qs[V])/float(scores[V]) for V in Vs}
avg_qc = {V: avg_qc[V]/(scores[V]*float(nc)) for V in Vs}
avg_qs = {V: avg_qs[V]/(scores[V]*float(ns)) for V in Vs}
avg_comm = {V: avg_comm[V]/scores[V] for V in Vs}
avg_comp = {V: avg_comp[V]/scores[V] for V in Vs}
total_cost = {V: avg_comm[V] + avg_comp[V] for V in Vs}


avg_qc = [avg_qc[V] for V in Vs]
avg_qs = [avg_qs[V] for V in Vs]
avg_comp = [avg_comp[V] for V in Vs]
avg_comm = [avg_comm[V] for V in Vs]
total_cost = [total_cost[V] for V in Vs]
total_qlen = [total_qlen[V] for V in Vs]

with codecs.open(filename + '/avg_qc', 'w+', 'utf-8') as f:
    cp.dump(f, avg_qc)

with codecs.open(filename + '/avg_qs', 'w+', 'utf-8') as f:
    cp.dump(f, avg_qs)

with codecs.open(filename + '/avg_comm', 'w+', 'utf-8') as f:
    cp.dump(f, avg_comm)

with codecs.open(filename + '/avg_comp', 'w+', 'utf-8') as f:
    cp.dump(f, avg_comp)

with codecs.open(filename + '/total_cost', 'w+', 'utf-8') as f:
    cp.dump(f, total_cost)

with codecs.open(filename + '/total_qlen', 'w+', 'utf-8') as f:
    cp.dump(f, total_qlen)
#
# with codecs.open(filename + '/Q_C_0', 'w+', 'utf-8') as f:
#     cp.dump(f, Q_C_0)
#
# with codecs.open(filename + '/Q_C_1', 'w+', 'utf-8') as f:
#     cp.dump(f, Q_C_1)
#
# with codecs.open(filename + '/Q_S_0', 'w+', 'utf-8') as f:
#     cp.dump(f, Q_S_0)
#
# if topo == 10:
#     with codecs.open(filename + '/Q_S_12', 'w+', 'utf-8') as f:
#         cp.dump(f, Q_S_12)
#
#     with codecs.open(filename + '/Q_S_24', 'w+', 'utf-8') as f:
#         cp.dump(f, Q_S_24)
#
# if topo == 60:
#     with codecs.open(filename + '/Q_S_25', 'w+', 'utf-8') as f:
#         cp.dump(f, Q_S_25)
#
#     with codecs.open(filename + '/Q_S_50', 'w+', 'utf-8') as f:
#         cp.dump(f, Q_S_50)

end = time.time()
print('It took', (end-start)/60, 'min(s) to run.')