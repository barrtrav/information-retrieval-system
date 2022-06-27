import sqlite3 as sq
from pathlib import Path
from corpus import CorpusAnalyzer

class DocumentRecommender:
    def __init__(self, analyzer:CorpusAnalyzer, ratings=None, django=False) -> None:
        self.django = django
        self.analyzer = analyzer
        self.name = analyzer.name
        if ratings is None:
            if django : self.load_dj_ratings()
            else: self.load_ratings()
        else:
            self.ratings = ratings

    @property
    def mean_of_items(self):
        return sum(self.ratings.values()) / len(self.ratings)

    def similarity(self, doc_i: int, doc_j: int) -> float:
        return self.jaccard_distance(doc_i, doc_j)

    def jaccard_distance(self, doc_i, doc_j):
        set_i = set(self.analyzer.mapping[doc_i].lexer)
        set_j = set(self.analyzer.mapping[doc_j].lexer)
        intersect = len(set_i.intersection(set_j))
        union = len(set_i.union(set_j))
        return intersect / union

    def add_rating(self, doc_id, rating):
        self.ratings[doc_id] = rating

        if self.django : self.save_dj_ratings()
        else: self.save_ratings()

    def add_ratings(self, ratings):
        self.ratings.update(ratings)
        
        if self.django : self.save_dj_ratings()
        else: self.save_ratings()

    def doc_deviation(self, doc_id):
        try:
            return self.ratings[doc_id] - self.mean_of_items
        except KeyError:
            return -self.mean_of_items

    def predictor_baseline(self, doc_id):
        return self.mean_of_items + self.doc_deviation(doc_id)

    def expected_rating(self, doc_id: int):
        documents = [doc_id for doc_id in self.analyzer.mapping]
        rated_documents = [doc_id for doc_id in documents if doc_id in self.ratings]
        numerator = sum(map(lambda d: self.similarity(doc_id, d)*(self.ratings[d] - self.predictor_baseline(d)), rated_documents))
        denominator = sum(map(lambda d: self.similarity(doc_id, d), rated_documents))
        try:
            return self.predictor_baseline(doc_id) + numerator / denominator
        except ZeroDivisionError:
            return 0
    
    def recommend_documents(self, k=5):
        doc_ratings = {}
        for doc_id in self.analyzer.mapping:
            if doc_id not in self.ratings:
                predicted_rating = self.expected_rating(doc_id)
                doc_ratings[doc_id] = predicted_rating
        return sorted(doc_ratings, key=lambda x: doc_ratings[x])[:k]

    def load_ratings(self):
        db_path = Path(f'../source/database/{self.name}.db')
        if not db_path.exists(): raise FileNotFoundError
        
        db = sq.connect(db_path)
        cursor = db.cursor()
        
        self.ratings = {}
        for id, value in cursor.execute('SELECT * FROM "index_ratings";'):
            self.ratings[id] = value

        db.close()

    def load_dj_ratings(self):
        from index.models import IndexRatings
        ratings = IndexRatings.objects.using(self.name).all()
        
        self.ratings = {}
        for rat in ratings:
            self.ratings[rat.id] = rat.value

    def save_ratings(self):
        db_path = Path(f'../source/database/{self.name}.db')
        if not db_path.exists(): raise FileNotFoundError

        db = sq.connect(db_path)

        for id in self.ratings:
            db.execute(f'INSERT OR REPLACE INTO "index_ratings" ("id", "value") values ({id}, "{self.ratings[id]}");')

        db.commit()
        db.close()

    def save_dj_ratings(self):
        from index.models import IndexRatings

        ratings = IndexRatings.objects.using(self.name)
        for id in self.ratings:
            try:
                rat = ratings.get(id=id)
                rat.value = self.ratings[id]
                rat.save(using=self.name)
            except IndexRatings.DoesNotExist:
                rat = IndexRatings(id=id, value=self.ratings[id])
                rat.save(using=self.name)

