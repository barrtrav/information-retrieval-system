from nltk.corpus import wordnet as wn
from typing import List, Dict
from nltk.corpus import words
from nltk.metrics.distance import edit_distance
from model import Model
from corpus import Corpus
from query import Query
import math
import json

def Expansion(query, model : Model, mode='hypernym') -> List[str]:
    expansion = LoadExpansion(query, model.corpus.name)
    if expansion is not None: return expansion
    v_query = Query().TextParse(query)
    tokens, change = SpellChecking(v_query)
    new_tokens = RelaxedQuery(v_query, model)
    if change: expansion = [tokens] + new_tokens
    else: expansion = new_tokens
    SaveExpansion(query, expansion, model.corpus.name)
    return expansion

def SpellChecking(tokens: List[str]) -> str:
    correct_words = words.words()
    correct_spelling = []
    change = False
    for token in tokens:
        temp = [(edit_distance(token, w), w) for w in correct_words if w[0] == token[0]]
        word = min(temp, key=lambda x: x[0])[1]
        if word != token:
            change = True
        correct_spelling.append(word)
    return " ".join(correct_spelling), change

def RelaxedQuery(tokens: List[str], model : Model) -> List[str]:
    threshold = math.log2(len(model.corpus.documents) / 10)
    alternatives = {}
    for i, token in enumerate(tokens):
        if token not in model.corpus.index.token2id or model.Idf(model.corpus.index.token2id[token]) > threshold:
            for element in wn.synsets(token):
                try:
                    try:alternatives[i].union(set(element.hypernyms()[0].lemma_names())).union(set(element.lemma_names()))
                    except KeyError:alternatives[i] = set(element.hypernyms()[0].lemma_names()).union(element.lemma_names())
                except IndexError:pass
    return AlternativeTokens(tokens, threshold, alternatives, model)

def AlternativeTokens(tokens: List[str], threshold: float, alternatives: Dict[int, set], model : Model):
    alternative_tokens = []
    for idx, alternatives in alternatives.items():
        for word in alternatives:
            temp = tokens.copy()
            term = temp[idx]
            if term is not word and term in model.corpus.index.token2id and \
                    model.Idf(model.corpus.index.token2id[term]) <= threshold:
                temp[idx] = word
                alternative_tokens.append(" ".join(temp))
    return alternative_tokens

def SaveExpansion(query : str, new_query, name : str = 'misc'):
    try: exp = json.load(open(f'../resource/expansion/{name}_exp.json', 'r+'))
    except FileNotFoundError: exp = {}
    exp[query] = new_query
    json.dump(exp, open(f'../resource/expansion/{name}_exp.json', 'w+'))

def LoadExpansion(query : str, name = 'misc'):
    try: 
        exp = json.load(open(f'../resource/expansion/{name}_exp.json', 'r+'))
        try: return exp[query]
        except: return None
    except FileNotFoundError:return None