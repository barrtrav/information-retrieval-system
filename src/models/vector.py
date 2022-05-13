import math
from models import ModelRI
from corpus import CorpusAnalyzer
from tools import Document, Token, TokenList

class VectorMRI(ModelRI):
    def __init__(self, analyzer: CorpusAnalyzer) -> None:
        self.a = 0.4
        super().__init__(analyzer)
        self.N = len(analyzer.documents)

    def ranking(self, query:dict, max_freq:int) -> list:
        ranking = []
        for i, doc in enumerate(self.analyzer.documents):
            num = 0
            doc_weights_sqr = 0
            query_weights_sqr = 0
            for lex in query:
                w_doc = self.weight_doc(self.analyzer.index.get(lex), doc)
                w_query = self.weight_query(lex, query[lex]/max_freq, self.analyzer.index)
                num += w_doc * w_query
                doc_weights_sqr += w_doc ** 2
                query_weights_sqr += w_query ** 2
            try:
                sim = num / (math.sqrt(doc_weights_sqr) * math.sqrt(query_weights_sqr))
            except ZeroDivisionError:
                sim = 0
            if sim > 0.3:
                ranking.append((doc, sim))
        ranking.sort(key=lambda x:x[1], reverse=True)
        return ranking

    def weight_query(self, lex:str, tf:float,  index:TokenList) -> float:
        return (self.a + (1 - self.a) * tf) * math.log(self.N / index.get(lex).ni)

    def weight_doc(self, token:Token, doc: Document) -> float:
        return token.tf(doc.id) * self.idf(token)

    def idf(self, token:Token) -> float:
        return math.log(self.N / token.ni)