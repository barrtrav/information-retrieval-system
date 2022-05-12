class RochioFeedBack:
    def __init__(self, query, analyzer, relevant_docs, non_relevant_doc) -> None:
        self.query = query
        self.analyzer = analyzer
        self.relevant_docs = relevant_docs
        self.non_relevant_doc = non_relevant_doc
