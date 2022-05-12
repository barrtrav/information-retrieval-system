from pathlib import Path
from system import IRSystem
from models import VectorMRI
from corpus import LisaCorpusAnalyzer

def make_query(query, system:IRSystem):
    #analyzer = system.analyzer
    print('Query for the ','parse.name',' parse')
    docs, ranking = system.make_query(query, get_ranking=True)
    print('First 20 results for the query:')
    for doc in docs[:20]:
        print(doc)
    #print("Doing pseudo-feedback")
    #system.pseudo_feedback(query, ranking)
    print("Documt recomendations")
    for doc in system.get_recommended_documents():
        print(doc)

def get_analyzer(name):
    if name == 'lisa':
        analyzer = LisaCorpusAnalyzer()
        return IRSystem(VectorMRI(analyzer))
    else:
        return None

if __name__ == '__main__':
    while True:
        name = 'lisa' #input('Please choose a corpus [cran, cisi, lisa, npl, wiki, all]:\n')
        system = get_analyzer(name)
        if system is None:
            print('Please choose a valid corpus')
            continue
        else:
            break
    query_text = """I WOULD BE INTERESTED TO RECEIVE INFORMATION ON NON-USERS OF LIBRARIES,
INCLUDING ANY STUDIES OF WHO ARE NON-USERS AND WHY THEY ARE NON-USERS.
I WOULD BE ESPECIALLY GRATEFUL FOR PAPERS GIVING THE METHODOLOGICAL
APPROACHES USED IN THESE STUDIES AND THE RESULTS OBTAINED.
NON-USE, LIBRARY USE, USER STUDIES."""#input('Make a query:\n')
    make_query(query_text, system)