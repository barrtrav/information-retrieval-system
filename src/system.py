import json
from typing import Any, List, Tuple
from model import Model
from query import Query, LoadQuery
from cluster import Cluster
from recom import Recommender
from utils import Document
from feedback import Feedback

class System:
    def __init__(self, model : Model):
        self.model = model 
        self.cluster = Cluster(model)
        self.recommender = Recommender(self.cluster, self.model.corpus)

    def MakeQuery(self, query : str):
        raise NotImplementedError

    def Recommend(self, ranking = None):
        raise NotImplementedError
    
    def AutoFeedBack(self, query, ranking = None):
        raise NotImplementedError

class VectorSystem(System):
    def __init__(self, model : Model) -> None :
        super().__init__(model)
        self.queryparse = Query()

    def MakeQuery(self, query : str):
        feed_query = LoadQuery(query, self.model.corpus.name)
        vect_query = self.queryparse(query, self.model.corpus.index) if feed_query is None else feed_query

        ranking = self.model.Ranking(vect_query)
        docs = self.model.Index2Documents(ranking)

        try:
            related = self.cluster.DocumentCluster(ranking[0][0])
            related = [self.model.corpus.documents[doc_id] for doc_id in related[:10]]
            docs = docs[:20] + [doc for doc in related if doc not in docs[:20]]
        except: pass

        if len(docs) > 0:
            self.recommender.AddRating(ranking[0][0])

        return docs, ranking

    def Recommend(self, ranking) -> List[Document]:
        if not len(self.recommender.ratings): return []
        recommend = [self.model.corpus.documents[doc_id] for doc_id in self.recommender.Recommend() if doc_id not in ranking]
        return recommend[:5]

    def AutoFeedBack(self, query : str, ranking : List[Tuple[int, float]], k=10):
        relevant = [doc_id for doc_id, _ in ranking[:k]]
        nonrelevant = [doc_id for doc_id, _ in ranking[k:]]
        Feedback(query, self.model.corpus, relevant, nonrelevant)
        self.recommender.AddRatings(relevant)

    def UserFeedBack(self, query : str, relevant, recobrado):
        nonrelevant = [doc_id for doc_id in recobrado if doc_id not in relevant]
        self.recommender.AddRating(relevant)
        Feedback(query, self.model.corpus, relevant, nonrelevant)
        self.recommender.AddRatings(relevant)

class BoolSystem(System):
    def __init__(self, model: Model):
        super().__init__(model)
        self.textparse = Query().TextParse

    def MakeQuery(self, query: str):
        feed_query = self.LoadParse(query)
        if feed_query is None:
            query = ' '.join(self.textparse(query))
        else: query = feed_query

        ranking = self.model.Ranking(query)
        docs = self.model.Index2Documents(ranking)

        try:
            related = self.cluster.DocumentCluster(ranking[0][0])
            related = [self.model.corpus.documents[doc_id] for doc_id in related[:10]]
            docs = docs[:20] + [doc for doc in related if doc not in docs[:20]]
        except: pass

        if len(docs) > 0:
            self.recommender.AddRating(ranking[0][0])

        return docs, ranking

    def Recommend(self, ranking) -> List[Document]:
        if not len(self.recommender.ratings): return []
        recommend = [self.model.corpus.documents[doc_id] for doc_id in self.recommender.Recommend() if doc_id not in ranking]
        return recommend[:5]

    def AutoFeedBack(self, query : str, ranking : List[Tuple[int, float]], k=10):       
        relevant = [doc_id for doc_id, _ in ranking[:k]]
        new_query = ' OR '.join(self.textparse(query))
        self.SaveParse(query, new_query)
        self.recommender.AddRatings(relevant)

    def LoadParse(self, query):
        try:
            queries = json.load(open(f'../resource/queries/{self.model.corpus.name}_query.json', 'r+'))
            try: return queries[query]
            except KeyError: return None
        except FileNotFoundError:return None

    def SaveParse(self, query, expansion):
        try:
            queries = json.load(open(f'../resource/queries/{self.model.corpus.name}_query.json', 'r+'))
        except FileNotFoundError:
            queries = {}
        queries[query] = expansion
        json.dump(queries, open(f'../resource/queries/{self.model.corpus.name}_query.json', 'w+'))
