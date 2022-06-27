import re
import json
from typing import List, Tuple
from utils import REGEX
from gensim.corpora import Dictionary
from nltk import PorterStemmer, wordpunct_tokenize
import nltk

class Query:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def TextParse(self, text : str) -> List[str]:  
        text = re.sub(REGEX, ' ', text)
        text = re.sub('\s+', ' ', text)
        text = text.lower()
        tokens = wordpunct_tokenize(text)
        tokens = [token for token in tokens if token not in self.stopwords]
        #tokens = [self.stemmer.stem(token) for token in tokens]
        return tokens

    def Vector(self, text : str, index : Dictionary) -> List[Tuple[int, int]]:
        return index.doc2bow(self.TextParse(text))

    def __call__(self, text : str, index : Dictionary) -> List[Tuple[int, int]]:
        return self.Vector(text, index)

def SaveQuery(query : str, v_query : List[Tuple[int, float]], name : str = 'misc') -> None:
    query = Query2Parse2Query(query)
    try:
        queries = json.load(open(f'../resource/queries/{name}_queries.json', 'r+'))
    except FileNotFoundError:
        queries = {}
    queries[query] = v_query
    json.dump(queries, open(f'../resource/queries/{name}_queries.json', 'w+'))

def LoadQuery(query : str, name = 'misc'):
    query = Query2Parse2Query(query)
    try: 
        queries = json.load(open(f'../resource/queries/{name}_queries.json', 'r+'))
        try: return queries[query]
        except: return None
    except FileNotFoundError:
        return None

def Query2Parse2Query(query : str):
    return ' '.join(Query().TextParse(query))