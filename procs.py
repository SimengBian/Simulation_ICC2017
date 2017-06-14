from random import *
td = [0, 0.08514851485148515, 0.15247524752475247, 0.19603960396039605, 0.2297029702970297, 0.2514851485148515, 0.26732673267326734, 0.28316831683168314, 0.2891089108910891, 0.297029702970297, 0.299009900990099, 0.30297029702970296, 0.3069306930693069, 0.41386138613861384, 0.49504950495049505, 0.592079207920792, 0.7346534653465346, 0.8138613861386138, 0.9603960396039604, 1.0]
xs = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 250, 400, 450, 650, 1000, 1600, 8000, 25000]
lenOfTS = 10000


def interval_generator(r):
    rand = random()
    for i in range(1, len(td)):
        if rand <= td[i]:
            interval = random()*(xs[i] - xs[i-1]) + xs[i-1]
            return interval/float(lenOfTS)
        else:
            continue
    raise Exception("It shouldn't reach here..")

procs = {
    'exp': (lambda lam: expovariate(lam)),
    'pareto': (lambda alpha: paretovariate(0.999*alpha+1)-1),
    'uni': (lambda r: uniform(0, 2.0/r)),
    'normal': (lambda r: max(0, normalvariate(1.0/r, 0.005))),
    'constant': (lambda r: 1.0/r),
    'trace': interval_generator
}


def generate(ns, s, arrProc, arrRate):

    lastPktTimes = {}
    lastPktTimes[s] = -1
    total = 1
    p = arrRate

    totalArrivals = 0

    if lastPktTimes[s] > 0:
        if lastPktTimes[s] > total:
           lastPktTimes[s] -= total
           total = -1
        else:
            total -= lastPktTimes[s]
            lastPktTimes[s] = -1
            totalArrivals += 1

    while total > 0: # Now last packet time == -1
        lastPktTimes[s] = arrProc(p)
        # print lastPktTimes[s]
        if lastPktTimes[s] > total:
            lastPktTimes[s] -= total
            total = -1
            break
        else:
            total -= lastPktTimes[s]
            lastPktTimes[s] = -1
            totalArrivals += 1

    return totalArrivals