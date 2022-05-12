from pathlib import Path
from system import IRSystem
from models import VectorMRI
from corpus import LisaCorpusAnalyzer, CranCorpusAnalyzer

def make_query(query, system:IRSystem):
    docs, ranking = system.make_query(query, get_ranking=True)
    print('First 20 results for the query:')
    for doc in docs[:20]:
        print(doc)

def get_analyzer(name):
    if name == 'lisa':
        analyzer = LisaCorpusAnalyzer()
        return IRSystem(VectorMRI(analyzer))
    elif name == 'cran':
        analyzer = CranCorpusAnalyzer()
        return IRSystem(VectorMRI(analyzer))
    else:
        return None

if __name__ == '__main__':
    while True:
        name = input('Please choose a corpus [cran, cisi, lisa, npl, wiki]:\n')
        system = get_analyzer(name)
        if system is None:
            print('Please choose a valid corpus')
            continue
        else:
            break
    while True:
        query_text =input('Make a query:\n')
        make_query(query_text, system)