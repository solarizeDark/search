import collections
import os

import spacy
from bs4 import BeautifulSoup

nlp = spacy.load('en_core_web_sm')
tokens = set()
lemmas = collections.defaultdict(set)
dirname = '../pages'
tokens_file = open('tokens.txt', 'w', encoding='utf-8')
for file in os.listdir(dirname):
	page = open(dirname + '/' + file, 'r', encoding='utf-8')
	soup = BeautifulSoup(page, 'html.parser')
	paragraphs = soup.find_all('p')
	for e in paragraphs:
		tokens_info = nlp(e.text)
		for token in tokens_info:
			token_lower = token.text.lower()
			if token.is_alpha and not token.is_stop and token_lower not in tokens:
				tokens.add(token_lower)
				tokens_file.write(token_lower + '\n')
				tokens_file.flush()

				lemmas[token.lemma_].add(token_lower)

tokens_file.close()

lemmas_file = open('lemmas.txt', 'w', encoding='utf-8')
for k, v in lemmas.items():
	lemmas_file.write(k + ': ' + ' '.join(lemmas[k]) + '\n')
	lemmas_file.flush()

lemmas_file.close()
print(len(lemmas))