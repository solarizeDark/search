from eldar import Query

full_list = [i for i in range(1, 339)]

def intersection(l1, l2):
	l3 = [value for value in l1 if value in l2]
	return l3

def difference(l1, l2):
	l3 = []
	for xl in l1:
		if xl not in l2:
			l3.append(xl)
	return l3

def union(l1, l2):
	return l1 + list(set(l2) - set(l1))

def get_tokens():
	tokens = {}
	with open('indexes.txt', encoding='utf-8') as file:
		for line in file:
			tokens[line[:line.index(':')]] = [int(x) for x in line[line.index(':') + 2:].split(' ')]
	return tokens

'''
	not	-
	and	&
	or	|
'''
def get_page_indexes(tokens, query):
	query = query.replace(' ', '')
	helper = {}
	cnt = 0

	# NOT
	while query.find('-') != -1:
		right = min([
			1e6 if query.find(' ', query.find('-')) == -1 else query.find(' ', query.find('-')),
			1e6 if query.find('&', query.find('-')) == -1 else query.find('&', query.find('-')),
			1e6 if query.find('|', query.find('-')) == -1 else query.find('|', query.find('-')),
			len(query)])
		token = query[query.find('-'): right]
		helper["h" + str(cnt)] = difference(full_list, tokens[token[1:]])
		query = query.replace(token, "h" + str(cnt))
		cnt+=1

	# AND
	while query.find('&') != -1:
		left = 0 if query.find('|') > query.find('&') or query.find('|') == -1 else len(query[:query.find('&')]) - query[:query.find('&')][::-1].find('|') - 1
		right = min([
			1e6 if query.find('|', query.find('&') + 1) == -1 else query.find('|', query.find('&') + 1),
			1e6 if query.find('&', query.find('&') + 1) == -1 else query.find('&', query.find('&') + 1),
			len(query)])

		step = query[0 if left == 0 else left + 1: right]
		loperand = step[:step.find('&')]
		roperand = step[step.find('&') + 1:]

		loperand = helper[loperand] if loperand in helper else tokens[loperand]
		roperand = helper[roperand] if roperand in helper else tokens[roperand]

		helper["h" + str(cnt)] = intersection(loperand, roperand)
		query = query.replace(step, "h" + str(cnt))
		cnt += 1

	# OR
	ors = query.split('|')
	res = []
	for token in ors:
		res = union(helper[token] if token in helper else tokens[token], res)

	return res

print(get_page_indexes(get_tokens(), 'things | blog & hands'))