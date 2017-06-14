from numpy import *

def dump(to, *obj):
	content = []
	for item in obj:
		content.append(str(item))
	if to is not None:
		to.write(str(content))
	# print('dumped:', content)

# with open('demo', 'w+', 'utf-8') as f:
# 	dump({1:2}, {2:3}, {3:4}, {4:5}, to=f)

def load(frm):
	if frm is not None:
		content = eval(frm.read().strip())
		results = []
		for item in content:
			# print item
			results.append(eval(item))
		return results
	else: return []

# with open('demo', 'r', 'utf-8') as f:
# 	results = load(f)
# 	print(results)
