import cp
import codecs
import numpy as np

topo = 10
parameter = '24' # 24, 48_48_10  4_8_10
arrProc = 'pareto' #exp normal pareto
condition = 'heter'
policy = 'greedy' # static, random, JSQ, greedy

configName = str(topo) + '_' + parameter + '_' + arrProc + '_' + condition

def lstToArr(lst):
    return np.array(lst)

with codecs.open('config/' + configName, 'r', 'utf-8') as f:
    config = cp.load(f)

print(config[0]['servRate'])
print(config[0]['As'])
# def lstToArr(lst):
#     return np.array(lst)
#
# with codecs.open('config/' + 'test', 'r', 'utf-8') as f:
#     config = cp.load(f)
#
# print lstToArr(config[0]['X'])