from pathlib import Path
from expansion import Expansion
from model import  VectorModel, BoolModel
from system import VectorSystem, BoolSystem
from corpus import  CranCorpus, CisiCorpus, LisaCorpus, NPLCorpus

from color import *

ALL_CORPUS_NAME = ['cran', 'cisi', 'lisa', 'npl']
ALL_MODEL_NAME = ['vector', 'bool']

def main() -> None:
    print(f'{CYAN}-- INFORMATION RETRIEVAL SYSTEM -- \n{RESET}')

    model_name = ''
    corpus_name = ''

    while model_name not in ALL_MODEL_NAME: 
        model_name = input(f'Choose a model name -> [{GREEN}vector{RESET}, {GREEN}bool{RESET}]: ')
    
    print()

    while corpus_name not in ALL_CORPUS_NAME: 
        corpus_name = input(f'Choose a corpus name -> [{GREEN}cran{RESET}, {GREEN}cisi{RESET}, {GREEN}lisa{RESET}, {GREEN}npl{RESET}]:')
   
    print()

    if corpus_name == 'npl': corpus = NPLCorpus()
    elif corpus_name == 'cran': corpus = CranCorpus()
    elif corpus_name == 'cisi': corpus = CisiCorpus()
    else : corpus = LisaCorpus()

    if model_name == 'vector': system = VectorSystem(VectorModel(corpus))
    else: system = BoolSystem(BoolModel(corpus))

    print(RESET + f'\nQuery for {system.model.corpus.name} corpus: \n' + RESET)

    while True:
        query = input(YELLOW + 'Make a Query: ' + RESET)
        print()

        docs, ranking = system.MakeQuery(query)
        print(f'{RED}[*]{RESET} First 20 results for the query:\n')
        for doc in docs: print(f'\t - ', doc)
        print()

        print(f'{RED}[*]{RESET} Make auto feedback\n')
        system.AutoFeedBack(query, ranking)

        (f'{RED}[*]{RESET} Query Expansion:')
        for exp in Expansion(query, system.model): print('\t - ', exp)
        print()

        print(f'{RED}[*]{RESET} Getting recommended documents:\n')
        for doc in system.Recommend([doc_id for doc_id, _ in ranking]):print('\t - ', doc)
        print()

if __name__ == '__main__':
    
    Path('../resource/').mkdir(exist_ok=True)
    Path('../resource/model/').mkdir(exist_ok=True)
    Path('../resource/corpus/').mkdir(exist_ok=True)
    Path('../resource/cluster/').mkdir(exist_ok=True)
    Path('../resource/recommend/').mkdir(exist_ok=True)
    Path('../resource/queries/').mkdir(exist_ok=True)
    Path('../resource/expansion/').mkdir(exist_ok=True)
    
    main()