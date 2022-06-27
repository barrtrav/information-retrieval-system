import pickle
import numpy as np

from pandas import DataFrame
from model import VectorModel
from sklearn.cluster import KMeans

from color import *

class Cluster:
    def __init__(self, model : VectorModel):
        self.model = model
        self.corpus = model.corpus
        
        try:
            self.LoadCluster()
            print(f'{RED}[-] Loaded Cluster{YELLOW}')
        except FileNotFoundError:
            print(f'{GREEN}[+] Building Cluster{RESET}')
            
            self.clusters = DataFrame()
            X = self.CreateDocumentVector()
            self.kmeans = KMeans(n_clusters=5)
            
            kmean = self.kmeans.fit(X)
            
            self.clusters['doc_id'] = list(range(X.shape[0]))
            self.clusters['cluster'] = kmean.labels_
            
            self.SaveCluster()

    def CreateDocumentVector(self):
        return np.array([self.GetDocumentVector(doc_id) for doc_id in range(len(self.corpus.documents))])

    def GetDocumentVector(self, doc_id : int):
        tfidf = np.zeros(len(self.corpus.index))
        for tok_id, _ in self.corpus.vectors[doc_id].items():
            tfidf[tok_id] = self.model.weight[(tok_id, doc_id)]
        return tfidf

    def SaveCluster(self) -> None:
        pickle.dump(self.kmeans, open(f'../resource/cluster/{self.corpus.name}_km.pkl', 'wb'))
        pickle.dump(self.clusters, open(f'../resource/cluster/{self.corpus.name}_df.pkl', 'wb'))

    def LoadCluster(self) -> None:
        self.kmeans = pickle.load(open(f'../resource/cluster/{self.corpus.name}_km.pkl', 'rb'))
        self.clusters = pickle.load(open(f'../resource/cluster/{self.corpus.name}_df.pkl', 'rb'))
        
    def PredictCluster(self, doc_id : int):
        return self.kmeans.predict(np.array([self.GetDocumentVector(doc_id)]))[0]

    def DocumentCluster(self, doc_id : int):
        return self.clusters[self.clusters.cluster == self.PredictCluster(doc_id)].doc_id.array