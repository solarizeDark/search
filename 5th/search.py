import math
import os


def get_tokens():
	tokens = {}
	with open('../3d/indexes.txt', encoding='utf-8') as file:
		for line in file:
			tokens[line[:line.index(':')]] = [int(x) for x in line[line.index(':') + 2:].split(' ')]
	return tokens

def get_token_vectors():
	# token_vectors - map with structure <page index>: [map <token>:(1 - idf)]
	token_vectors = {}
	for file in os.listdir('../tf-idf/tokens/'):
		with open('../tf-idf/tokens/' + file, 'r', encoding='utf-8') as tokens_file:
			token_vector = {}
			for line in tokens_file:
				parts = line.rstrip().split(' ')
				token_vector[parts[0]] = 1 - float(parts[2])

			token_vectors[int(file[:file.index('-')])] = token_vector

	return token_vectors

'''
	not	-
	and	&
	or	|
'''
def get_query_vectors(tokens, query):
	query = query.replace(' ', '')

	res_vectors = []

	# NOT
	while query.find('-') != -1:
		right = min([
			1e6 if query.find(' ', query.find('-')) == -1 else query.find(' ', query.find('-')),
			1e6 if query.find('&', query.find('-')) == -1 else query.find('&', query.find('-')),
			1e6 if query.find('|', query.find('-')) == -1 else query.find('|', query.find('-')),
			len(query)])
		token = query[query.find('-'): right]
		# 10 - huge wight to get page indexes to the bottom of result list
		res_vectors.append({tokens[token[1:]] : 10})
		query = query.replace(token, '')

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

		res_vectors.append({loperand: 1, roperand: 1})
		query = query.replace(step, '')

	# OR
	ors = query.split('|')
	ors_d = {}
	for token in ors:
		if token != '':
			ors_d[token] = 1
	res_vectors.append(ors_d)

	return res_vectors

res_vectors = get_query_vectors(get_tokens(), 'things | blog & hands')
token_vectors = get_token_vectors()

res = {}
for id, token_vector in token_vectors.items():
	euclidian_distance = 0
	for token_from_list, token_weight in token_vector.items():
		for vector in res_vectors:
			if token_from_list in vector:
				euclidian_distance += pow((vector[token_from_list] - token_weight), 2)
			else:
				euclidian_distance += 1
	res[id] = math.sqrt(euclidian_distance)

# sorted by distance from query indexes
res = dict(sorted(res.items(), key= lambda item: item[1]))
