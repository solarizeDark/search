import collections
import os

import spacy
from bs4 import BeautifulSoup

nlp = spacy.load('en_core_web_sm')
indexes = collections.defaultdict(set)
dirname = '../pages'

for file in os.listdir(dirname):
    page = open(dirname + '/' + file, 'r', encoding='utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    paragraphs = soup.find_all('p')
    for e in paragraphs:
        tokens_info = nlp(e.text)
        for token in tokens_info:
            token_lower = token.text.lower()
            if token.is_alpha and not token.is_stop:
                indexes[token_lower].add(file[:file.index('.')])

index_file = open('indexes.txt', 'w', encoding='utf-8')
for k, v in indexes.items():
    index_file.write(k + ': ' + ' '.join(indexes[k]) + '\n')
    index_file.flush()

index_file.close()