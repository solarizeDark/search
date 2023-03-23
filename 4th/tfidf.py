import collections
import os
from pathlib import Path
import spacy
from bs4 import BeautifulSoup
import math

def tf_idfs(dirname, idfs):
    for file in os.listdir(dirname):
        lines = []
        with open(dirname + file, 'r', encoding='utf-8') as t:
            for line in t:
                token = line.rstrip().split(' ')[0]
                token_tf = float(line.rstrip().split(' ')[1])
                lines.append(line.rstrip() + ' ' + str(math.log(DOCS_AMOUNT / idfs[token]) * token_tf) + '\n')
            t.close()
        with open(dirname + file, 'w', encoding='utf-8') as t:
            for l in lines:
                t.write(l)
                t.flush()
            t.close()

# <token, docs cnt>
tokens_idfs = {}
lemmas_idfs = {}

DOCS_AMOUNT = 338

with open('../2nd/tokens.txt', 'r', encoding='utf-8') as tokens_file:
    for line in tokens_file:
        tokens_idfs[line.rstrip()] = 0

with open('../2nd/lemmas.txt', 'r', encoding='utf-8') as tokens_file:
    for line in tokens_file:
        lemmas_idfs[line.rstrip().split(':')[0]] = 0

nlp = spacy.load('en_core_web_sm')
dirname = '../pages'
for file in os.listdir(dirname):

    tused = set()
    lused = set()

    tokens = {}
    lemmas = {}

    page = open(dirname + '/' + file, 'r', encoding='utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    paragraphs = soup.find_all('p')
    for e in paragraphs:
        tokens_info = nlp(e.text)
        for token in tokens_info:
            token_lower = token.text.lower()
            if token.is_alpha and not token.is_stop:
                if token_lower in tokens:
                    tokens[token_lower] = tokens[token_lower] + 1
                else:
                    tokens[token_lower] = 1
                if token.lemma_ in lemmas:
                    lemmas[token.lemma_] = lemmas[token.lemma_] + 1
                else:
                    lemmas[token.lemma_] = 1

                if not token_lower in tused:
                    tused.add(token_lower)
                    if token_lower in tokens_idfs:
                        tokens_idfs[token_lower] = tokens_idfs[token_lower] + 1
                    else:
                        tokens_idfs[token_lower] = 1

                if not token.lemma_ in lused:
                    lused.add(token.lemma_)
                    if token.lemma_ in lemmas_idfs:
                        lemmas_idfs[token.lemma_] = lemmas_idfs[token.lemma_] + 1
                    else:
                        lemmas_idfs[token.lemma_] = 1

    file_name = Path(dirname + '/' + file).stem
    with open('../tf-idf/tokens/' + file_name + '-t.txt', 'w', encoding='utf-8') as t:
        for k, v in tokens.items():
            t.write(k + ' ' + str(v / len(tokens.keys())) + '\n')
            t.flush()
    with open('../tf-idf/lemmas/' + file_name + '-l.txt', 'w', encoding='utf-8') as l:
        for k, v in lemmas.items():
            l.write(k + ' ' + str(v / len(lemmas.keys())) + '\n')
            l.flush()

tf_idfs('../tf-idf/tokens/', tokens_idfs)
tf_idfs('../tf-idf/lemmas/', lemmas_idfs)
