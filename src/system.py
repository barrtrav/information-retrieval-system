from models import ModelRI
from utils import query_parse
from recommender import DocumentRecommender

class IRSystem:
    def __init__(self, model:ModelRI, django=False) -> None:
        self.model = model
        self.analyzer = model.analyzer
        self.document_recommender = DocumentRecommender(self.analyzer, django=django)

    def make_query(self, query_text, get_ranking=False):
        query, max_freq = query_parse(query_text)

        doc_ranking = self.model.ranking(query, max_freq)
        docs = self.model.similarity(doc_ranking)

        if len(docs) > 0:
            self.document_recommender.add_rating(docs[0].id, 1)
    
        if get_ranking:
            return docs, doc_ranking
        else:
            return docs

    def get_recommended_documents(self) :
        """
        Returns the 5 more interesting useen documents for the user
        according to the recommendation system
        """
        # If there is no rated document return zero
        if len(self.document_recommender.ratings) == 0:
            return []
        docs_id = self.document_recommender.recommend_documents(5)
        return [id for id in docs_id]