import math
import pickle

from corpus import Corpus
from utils import Document
from pathlib import Path
from typing import List, Tuple, Dict

from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.qparser import QueryParser

from color import *

class Model:
    def __init__(self, corpus : Corpus) -> None:
        self.corpus : Corpus = corpus

    def Index2Documents(self, ranking : List[Tuple[int, float]]) -> List[Document]:
        return [self.corpus.documents[doc_id] for doc_id, _ in ranking]

    def Ranking(self, vect_query : List[Tuple[int, int]]) -> List[Tuple[int, float]]:
        raise NotImplementedError
    
class VectorModel(Model):
    def __init__(self, corpus: Corpus, a : float = 0.4) -> None:
        super().__init__(corpus)
        self.CreateWeightVect()
        self.a = a

    def Index2Documents(self, ranking : List[Tuple[int, float]]) -> List[Document]:
        return [self.corpus.documents[doc_id] for doc_id, _ in ranking]

    def Ranking(self, vect_query : List[Tuple[int, int]]) -> List[Tuple[int, float]]:
        ranking = []
        vect_query = dict(vect_query)
        
        for doc_id, doc in enumerate(self.corpus.documents):
            n = 0
            wd_sqrt = 0
            wq_sqrt = 0

            for tok_id in vect_query:
                wd = self.WeightDocument(tok_id, doc_id)
                wq = self.WeightQuery(tok_id, vect_query)
                
                n += wd * wq
                
                wd_sqrt += wd ** 2
                wq_sqrt += wq ** 2

            try:similitud = n / (math.sqrt(wd_sqrt) * math.sqrt(wq_sqrt))
            except ZeroDivisionError: similitud = 0

            if similitud > 0.3: ranking.append((doc_id, similitud))
        
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking

    def CreateWeightVect(self) -> None:
        self.weight = self.LoadWeight()
        
        if self.weight : 
            print(f'{RED}[-] Loaded Model{RESET}')
            return
        else: print(f'{GREEN}[+] Building Model{RESET}')
        
        for doc_id, doc in enumerate(self.corpus.documents):
            for token in doc.tokens:
                tok_id = self.corpus.index.token2id[token]
                self.weight[(tok_id, doc_id)] = self.WeightDocument(tok_id, doc_id)
        
        self.SaveWeight()

    def WeightDocument(self, tok_id : int, doc_id : int) -> float:
        return self.Tf(tok_id, doc_id) * self.Idf(tok_id)

    def WeightQuery(self, tok_id : int, vect_query : Dict[int, int]) -> float:
        return (self.a + (1 - self.a) * (vect_query[tok_id] / max(vect_query.values()))) * self.Idf(tok_id)

    def Tf(self, tok_id : int, doc_id : int) -> float:
        return self.corpus.Freq(tok_id, doc_id) / self.corpus.MaxFreq(doc_id)

    def Idf(self, tok_id : int) -> float:
        return math.log2(len(self.corpus.documents) / self.corpus.index.dfs[tok_id])

    def LoadWeight(self) -> Dict[Tuple[int, int], float]:
        try: return pickle.load(open(f'../resource/model/{self.corpus.name}_weight.pkl', 'rb'))
        except FileNotFoundError: return {}

    def SaveWeight(self) -> None:
        pickle.dump(self.weight, open(f'../resource/model/{self.corpus.name}_weight.pkl', 'wb'))

class BoolModel(Model):
    def __init__(self, corpus : Corpus):
        super().__init__(corpus)
        self.weight = self.LoadWeight()

        try:
            self.index = open_dir(f'../resource/model/{self.corpus.name}_index/')
            print(RED + '[-] Loaded Model' + RESET)
        except EmptyIndexError:
            print(GREEN + '[+] Building Model' + RESET)
            Path(f'../resource/model/{self.corpus.name}_index/').mkdir(exist_ok=True)
            schema = Schema(title=TEXT(stored=True), id=NUMERIC(stored=True), text=TEXT(stored=True))
            self.index = create_in(f'../resource/model/{self.corpus.name}_index/', schema)
            self.LoadDocuemnts()

    def LoadDocuemnts(self):
        write = self.index.writer()
        for i, doc in enumerate(self.corpus.documents):
            write.add_document(title=doc.title, id=i, text=doc.text)
        write.commit()

    def Ranking(self, text: str):
        with self.index.searcher() as searcher:
            query = QueryParser('text', self.index.schema).parse(text)
            results = searcher.search(query)
            return [(doc['id'], 1) for doc in results]

    def LoadWeight(self) -> Dict[Tuple[int, int], float]:
        try: return pickle.load(open(f'../resource/model/{self.corpus.name}_bool.pkl', 'rb'))
        except FileNotFoundError:
            weight = {}
            for doc_id in range(len(self.corpus.documents)):
                for tok_id in self.corpus.vectors[doc_id]:
                    try: weight[(tok_id, doc_id)]
                    except KeyError: weight[(tok_id, doc_id)] = 1
            pickle.dump(weight, open(f'../resource/model/{self.corpus.name}_bool.pkl', 'wb'))
            return weight

    def Tf(self, tok_id : int, doc_id : int) -> float:
        return 1

    def Idf(self, tok_id : int) -> float:
        return 1
