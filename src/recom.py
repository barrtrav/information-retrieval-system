from typing import Dict, List
from corpus import Corpus
from cluster import Cluster
import json

class Recommender:
    def __init__(self, cluster : Cluster, corpus : Corpus, ratings : Dict[int, int] = None) -> None:
        self.corpus = corpus
        self.cluster = cluster
        self.ratings = self.LoadRating()

    @property
    def Mean(self):
        return sum(self.ratings.values()) / len(self.ratings)

    def Jaccard(self, doc_i : int, doc_j : int) -> float:
        vec_i = set(self.corpus.vectors[doc_i])
        vec_j = set(self.corpus.vectors[doc_j])
        return len(vec_i.intersection(vec_j)) / len(vec_j.union(vec_j))
        
    def AddRating(self, doc_id : int) -> None: 
        try:self.ratings[str(doc_id)] += 1
        except KeyError: self.ratings[str(doc_id)] = 1
        
        self.SaveRating()

    def AddRatings(self, ratings : List[int]) -> None:
        for doc_id in ratings:
            try: self.ratings[str(doc_id)] += 1
            except KeyError: self.ratings[str(doc_id)] = 1
        self.SaveRating()

    def Deviation(self, doc_id : int):
        try:return self.ratings[str(doc_id)] - self.Mean
        except: return - self.Mean

    def BaseLine(self, doc_id : int):
        return self.Mean + self.Deviation(doc_id)

    def RatingPredict(self, doc_id : int):
        documents = self.cluster.DocumentCluster(doc_id)
        rated = [doc_id for doc_id in documents if str(doc_id) in self.ratings]
        
        term_a = sum(map(lambda doc: self.Jaccard(doc_id, doc) * (self.ratings[str(doc)] ), rated))
        term_b = sum(map(lambda doc: self.Jaccard(doc_id, doc), rated))

        try:
            return term_a / term_b
        except ZeroDivisionError: 
            return 0

    def Recommend(self, k=5):
        ratings = {}
        for doc_id in range(len(self.corpus.documents)):
            try: self.ratings[str(doc_id)]
            except KeyError:ratings[doc_id] = self.RatingPredict(doc_id)
        return sorted(ratings, key=lambda x: ratings[x], reverse=True)[:20 + k]
    
    def LoadRating(self):
        try: 
            return json.load(open(f'../resource/recommend/{self.corpus.name}_ratings.json', 'r'))
        except FileNotFoundError: 
            return {}

    def SaveRating(self):
        json.dump(self.ratings, open(f'../resource/recommend/{self.corpus.name}_ratings.json', 'w'))