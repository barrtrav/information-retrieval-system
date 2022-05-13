from corpus import CorpusAnalyzer

class ModelRI:
    def __init__(self, analyzer:CorpusAnalyzer) -> None:
        self.analyzer = analyzer

    def ranking(self, query:dict, max_freq:int) -> list:
        raise NotImplementedError
    
    def similarity(self, ranking) -> list:
        return [id for id,_ in ranking]