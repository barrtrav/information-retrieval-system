from corpus import *
from model import VectorModel, BoolModel
from system import VectorSystem, BoolSystem, System
import evaluation
import json
import re
from color import *

class Test:
    def __init__(self, name = 'test'):
        self.name = name

        try:
            self.LoadTest()
            print(RED + '[-] Loaded Test' + RESET)
        except FileNotFoundError:
            print(GREEN + '[+] Building Test' + RESET)
            self.queries = self.ParseQuery()
            self.similarity = self.ParseSimilarity()
            self.SaveTest()

    def SaveTest(self):
        json.dump(self.queries, open(f'../resource/test/{self.name}_queries.json', 'w+'))
        json.dump(self.similarity, open(f'../resource/test/{self.name}_sim_queries.json', 'w+'))

    def LoadTest(self):
        self.queries = json.load(open(f'../resource/test/{self.name}_queries.json', 'r+'))
        self.similarity = json.load(open(f'../resource/test/{self.name}_sim_queries.json', 'r+'))

    def ParseQuery(self):
        raise NotImplementedError

    def ParseSimilarity(self):
        raise NotImplementedError

    def TestModel(self, system : System):
        print(BLUE + f'\n[...] Run {system.model.corpus.name} Test\n' + RESET)

        total = [0, 0, 0]
        count = 0
        for query_id, text in self.queries.items():

            print(RED + f'* Running... {query_id}/{len(self.queries)}' + RESET)
            
            try:doc_id_relevans = [int(doc_id) for doc_id in self.similarity[query_id].keys()]
            except KeyError: continue
            
            docs, ranking = system.MakeQuery(text)
            doc_id_recall = [doc.id for doc in docs[:len(doc_id_relevans)]]
            
            try:precision = evaluation.precision_score(doc_id_relevans, doc_id_recall)
            except ZeroDivisionError: precision = 0

            try:recall = evaluation.recall_score(doc_id_relevans, doc_id_recall)
            except ZeroDivisionError: recall = 0

            try:f1 = evaluation.f1_score(doc_id_relevans, doc_id_recall)
            except ZeroDivisionError: f1 = 0

            system.AutoFeedBack(text, ranking)
            
            total[0] += precision
            total[1] += recall
            total[2] += f1

            count += 1
        
        print(GREEN + f'\n [+] Result:' + RESET)

        print('\t - Precision: ', total[0]/count)
        print('\t - Recall: ', total[1]/count)
        print('\t - F1: ', total[2]/count)        

class CranTest(Test):
    def __init__(self):
        super().__init__('cran')

    def ParseQuery(self):
        id_regex = re.compile(r'\.I (\d+)')
        lines = open('../data/cran/cran.qry', 'r').readlines() + ['.I 0']

        queries = {}
        current_id  = None
        current_line = []

        getting_words = False
        count = 1
        for line in lines:
            match = id_regex.match(line)
            if match is not None:
                if len(current_line) > 0:
                    queries[current_id] = ' '.join(current_line)
                    count += 1
                current_id = count
                current_line = []
                getting_words = False
            elif line.startswith('.W'):
                getting_words = True
            elif getting_words:
                current_line.append(line)
        return queries

    def ParseSimilarity(self):
        lines = open(f'../data/cran/cranqrel', 'r').readlines()

        similarity = {}
        line_regex = re.compile(r'(\d+) (\d+) (-?\d+)')
        for line in lines:
            match = line_regex.match(line)
            if match is not None:
                q_id = int(match.group(1))
                doc_id = int(match.group(2))
                relevance = int(match.group(3))
                try:
                    similarity[q_id][doc_id] = relevance
                except KeyError:
                    try:
                        similarity[q_id].update({doc_id : relevance})
                    except KeyError:
                        similarity[q_id] = {doc_id : relevance}
        for query in similarity.keys():
            similarity[query] = dict(sorted(similarity[query].items(), key=lambda x: x[1]))
        return similarity

class CisiTest(Test):
    def __init__(self):
        super().__init__('cisi')

    def ParseQuery(self):
        id_regex = re.compile(r'\.I (\d+)')
        lines = open('../data/cisi/CISI.QRY', 'r').readlines() + ['.I 0']

        queries = {}
        current_id  = None
        current_line = []

        getting_words = False
        count = 1
        for line in lines:
            match = id_regex.match(line)
            if match is not None:
                if len(current_line) > 0:
                    queries[current_id] = ' '.join(current_line)
                    count += 1
                current_id = count
                current_line = []
                getting_words = False
            elif line.startswith('.W'):
                getting_words = True
            elif line.startswith('.B'):
                getting_words = False
            elif getting_words:
                current_line.append(line)
        return queries
    
    def ParseSimilarity(self):
        lines = open(f'../data/cisi/CISI.REL', 'r').readlines()

        similarity = {}
        line_regex = re.compile('\s+(\d+)\s+(\d+)')
        for line in lines:
            match = line_regex.match(line)
            if match is not None:
                q_id = int(match.group(1))
                doc_id = int(match.group(2))
                relevance = 0
                try:
                    similarity[q_id][doc_id] = relevance
                except KeyError:
                    try:
                        similarity[q_id].update({doc_id : relevance})
                    except KeyError:
                        similarity[q_id] = {doc_id : relevance}
        #new_dic = {}
        #
        # for k in similarity:
        #    new_dic[len(new_dic)+1] = similarity[k]
        return similarity#new_dic    

class LisaTest(Test):
    def __init__(self):
        super().__init__('lisa')

    def ParseQuery(self):
        id_regex = re.compile(r'(\d+)')
        lines = open('../data/lisa/LISA.QUE', 'r').readlines() + ['0']

        queries = {}
        current_id  = None
        current_line = []

        for line in lines:
            match = id_regex.match(line)
            if match is not None:
                if len(current_line) > 0:
                    queries[current_id] = ' '.join(current_line)
                current_id = int(match.group(1))
                current_line = []
            else:
                current_line.append(line[:-1])
        return queries

    def ParseSimilarity(self):
        lines = open(f'../data/lisa/LISA.REL', 'r').readlines()
        
        similarity = {}
        test_regex = re.compile(r'Query (\d+)')
        rel_regex = re.compile(r'\d+ Relevant Refs:')

        query_id: int = None
        next_line_is_doc = False
        for line in lines:
            match = test_regex.match(line)
            if match is not None:
                query_id = int(match.group(1))
            elif rel_regex.match(line) is not None:
                next_line_is_doc = True
            elif next_line_is_doc:
                docs_ids = [int(word) for word in line.split()[:-1]]
                for doc_id in docs_ids:
                    relevance = 0
                    try:
                        similarity[query_id][doc_id] = relevance
                    except KeyError:
                        try:
                            similarity[query_id].update({doc_id : relevance})
                        except KeyError:
                            similarity[query_id] = {doc_id : relevance}
                next_line_is_doc = False
        return similarity

class NPLTest(Test):
    def __init__(self):
        super().__init__('npl')

    def ParseQuery(self):
        id_regex = re.compile('(\d+)')
        lines = open('../data/npl/query-text', 'r').readlines() + ['0']

        queries = {}
        query_id  = None
        current_line = []

        for line in lines:
            match = id_regex.match(line)
            if match is not None:
                query_id = int(match.group(1))
            elif line.endswith('/\n'):
                queries[query_id] = ' '.join(current_line)
                current_line = []
            else:
                current_line.append(line)
        return queries

    def ParseSimilarity(self):
        lines = open('../data/npl/rlv-ass', 'r').readlines() + ['0']
        similarity = {}
        line_regex = re.compile('(\d+)')
        current_docs = []
        query_id = 0
        for line in lines:
            match = line_regex.match(line)
            if match is not None:
                query_id = int(match.group(1))
            elif line.endswith('/\n'):
                for doc_id in current_docs:
                    relevance = 0
                    try:
                        similarity[query_id][doc_id] = relevance
                    except KeyError:
                        try:
                            similarity[query_id].update({doc_id : relevance})
                        except KeyError:
                            similarity[query_id] = {doc_id : relevance}
                current_docs = []
            else:
                current_docs += [int(word) for word in line.split()]
        return similarity

ALL_CORPUS_NAME = ['cran', 'cisi', 'lisa', 'npl', 'all']
ALL_MODEL_NAME = ['vector', 'bool']

def test() -> None:
    print(f'{CYAN}-- TEST - INFORMATION RETRIEVAL SYSTEM -- \n{RESET}')

    model_name = ''
    corpus_name = ''

    while model_name not in ALL_MODEL_NAME: 
        model_name = input(f'Choose a model name -> [{GREEN}vector{RESET}, {GREEN}bool{RESET}]: ')
    
    print()

    while corpus_name not in ALL_CORPUS_NAME: 
        corpus_name = input(f'Choose a corpus name -> [{GREEN}cran{RESET}, {GREEN}cisi{RESET}, {GREEN}lisa{RESET}, {GREEN}npl{RESET}, {GREEN}all{RESET}]:')
   
    print()

    systems = []
    tests = []

    if corpus_name == 'npl' or corpus_name == 'all': 
        systems.append(NPLCorpus())
        tests.append(NPLTest())
    elif corpus_name == 'cran' or corpus_name == 'all':
        systems.append(CranCorpus())
        tests.append(CranTest())
    elif corpus_name == 'cisi' or corpus_name == 'all': 
        systems.append(CisiCorpus())
        tests.append(CisiTest())
    elif corpus_name == 'lisa' or corpus_name == 'all': 
        systems.append(LisaCorpus())
        tests.append(LisaTest())

    for i in range(len(systems)):
        if model_name == 'vector': systems[i] = VectorSystem(VectorModel(systems[i]))
        else: systems[i] = BoolSystem(BoolModel(systems[i]))

    for syst, test_model in zip(systems, tests):
        test_model.TestModel(syst)

if __name__ == '__main__':
    
    Path('../resource/').mkdir(exist_ok=True)
    Path('../resource/model/').mkdir(exist_ok=True)
    Path('../resource/corpus/').mkdir(exist_ok=True)
    Path('../resource/cluster/').mkdir(exist_ok=True)
    Path('../resource/recommend/').mkdir(exist_ok=True)
    Path('../resource/queries/').mkdir(exist_ok=True)
    Path('../resource/expansion/').mkdir(exist_ok=True)
    Path('../resource/test/').mkdir(exist_ok=True)
    
    test()