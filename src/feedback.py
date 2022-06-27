from corpus import Corpus
from typing import List, Dict, Tuple
from query import Query, SaveQuery

class Feedback:
    def __init__(self, query : str, corpus : Corpus, relevant : List[int], nonrelevant : List[int]) -> None:
        self.corpus = corpus
        self.relevant = relevant
        self.nonrelevant = nonrelevant
        self.v_query = Query().Vector(query, corpus.index)
        #self.d_query = dict(self.v_query)
        self.MakeFeedback(query)

    def Sum(self, docs) -> Dict[int, int]:
        sumdoc = {}
        for doc_id in docs:
            for tok_id, freq in self.corpus.vectors[doc_id].items():
                try: sumdoc[tok_id] += freq
                except KeyError:sumdoc[tok_id] = freq
        return sumdoc

    @staticmethod
    def SumVectors(vect_1 : Dict[int, int], vect_2 : Dict[int, int]) -> Dict[int, int]:
        for tok_id, freq in vect_2.items():
            try: vect_1[tok_id] += freq
            except KeyError: vect_1[tok_id] = freq
        return vect_1

    @staticmethod
    def ReduceDimension(v_query: Tuple[Tuple[int, int]], epsilon = 0.05):
        new_query = {}
        for tok_id, weight in v_query:
            if abs(weight) > epsilon:
                new_query[tok_id] = weight
        return list(new_query.items())

    def MakeFeedback(self, query, alpha=1, beta=0.75, gamma=0.15):
        n = len(self.relevant)
        term_1 = {tok_id : alpha * freq for tok_id, freq in self.v_query}
        term_2 = {tok_id : (beta / n) * freq for tok_id, freq in self.Sum(self.relevant).items()}
        
        n = len(self.nonrelevant)
        term_3 = {tok_id : (gamma / n) * freq for tok_id, freq in self.Sum(self.nonrelevant).items()}
        
        new_query = self.SumVectors(self.SumVectors(term_1, term_2), term_3)
        new_query = self.ReduceDimension(new_query.items())
        new_query.sort(key=lambda x:x[1], reverse=True)
        SaveQuery(query, new_query[:len(self.v_query)*2], self.corpus.name)
