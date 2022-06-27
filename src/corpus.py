from os import listdir
import re
import pickle
from typing import List
from pathlib import Path
from utils import Document, REGEX, STOPWORDS
from nltk import wordpunct_tokenize, PorterStemmer
from gensim.corpora import Dictionary
import nltk

from color import *

class Corpus:
    def __init__(self, name : str = 'corpus') -> None:
        self.name = name
        self.stemmer = PorterStemmer()
        self.documents : List[Document] = []
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

        try:
            self.LoadCorpus()
            print(f'{RED}[-] Loaded Corpus{RESET}')
        except FileNotFoundError:
            print(f'{GREEN}[+] Building Corpus{RESET}')
            self.DocumentParser()
            self.index = Dictionary([doc.tokens for doc in self.documents])
            self.vectors = [dict(self.index.doc2bow(doc.tokens)) for doc in self.documents]
            self.SaveCorpus()
        
    def DocumentParser(self):
        raise NotImplementedError

    def TextParse(self, text : str) -> List[str]:
        text = re.sub(REGEX, ' ', text)
        text = re.sub('\s+', ' ', text)
        text = text.lower()
        tokens = wordpunct_tokenize(text)
        tokens = [token for token in tokens if token not in self.stopwords]
        #tokens = [self.stemmer.stem(token) for token in tokens]
        return tokens

    def Freq(self, tok_id : int, doc_id : int) -> int:
        try:return self.vectors[doc_id][tok_id]
        except KeyError: return 0

    def MaxFreq(self, doc_id : int) -> int:
        return max(self.vectors[doc_id].items(), key=lambda x: x[1])[1]

    def LoadCorpus(self):
        self.index = Dictionary.load(f'../resource/corpus/{self.name}_index.idx')
        self.vectors = pickle.load(open(f'../resource/corpus/{self.name}_vects.pkl', 'rb'))
        self.documents = pickle.load(open(f'../resource/corpus/{self.name}_docs.pkl', 'rb'))

    def SaveCorpus(self):
        self.index.save(f'../resource/corpus/{self.name}_index.idx')
        pickle.dump(self.vectors, open(f'../resource/corpus/{self.name}_vects.pkl', 'wb'))
        pickle.dump(self.documents, open(f'../resource/corpus/{self.name}_docs.pkl', 'wb'))

class CranCorpus(Corpus):
    def __init__(self):
        super().__init__(name = 'cran')

    def DocumentParser(self):
        lines = open('../data/cran/cran.all.1400', 'r').readlines() + ['.I 0']
        id_regex = re.compile(r'\.I (\d+)')
        
        current_id : int = None
        current_lines : list = []
        current_title : list = []
        
        getting_words : bool = False
        getting_title : bool = False
        
        for line in lines:
            match = id_regex.match(line)
            
            if match is not None:
                if len(current_lines) > 0:
                    text = ' '.join(current_lines)
                    tokens = self.TextParse(text)
                    title = ' '.join(current_title)
                    title = title[0].capitalize() + title[1:-1]
                    self.documents.append(Document(current_id, title, tokens, text))
                
                current_lines = []
                current_title = []
                getting_words = False
                current_id = int(match.group(1))
            
            elif line.startswith('.T'):
                getting_title = True
            elif line.startswith('.W'):
                getting_words = True
            elif line.startswith('.A'):
                getting_title = False
            elif line.startswith('.X'):
                getting_words = False
            elif getting_words:
                current_lines.append(line[:-1])
            elif getting_title:
                current_title.append(line[:-1])

class CisiCorpus(Corpus):
    def __init__(self):
        super().__init__(name = 'cisi')

    def DocumentParser(self):
        lines = open('../data/cisi/CISI.ALL', 'r').readlines() + ['.I 0']
        id_regex = re.compile(r'\.I (\d+)')
        
        current_id : int = None
        current_lines : list = []
        current_title : list = []
        
        getting_words : bool = False
        getting_title : bool = False
        
        for line in lines:
            match = id_regex.match(line)
            
            if match is not None:
                if len(current_lines) > 0:
                    text = ' '.join(current_lines)
                    tokens = self.TextParse(text)
                    title = ' '.join(current_title)
                    title = title[0].capitalize() + title[1:-1]
                    self.documents.append(Document(current_id, title, tokens, text))
                
                current_lines = []
                current_title = []
                getting_words = False
                current_id = int(match.group(1))
            
            elif line.startswith('.T'):
                getting_title = True
            elif line.startswith('.W'):
                getting_words = True
            elif line.startswith('.A'):
                getting_title = False
            elif line.startswith('.X'):
                getting_words = False
            elif getting_words:
                current_lines.append(line[:-1])
            elif getting_title:
                current_title.append(line[:-1])

class LisaCorpus(Corpus):
    def __init__(self):
        super().__init__(name = 'lisa')

    def DocumentParser(self):
        id_regex = re.compile('Document\s+(\d+)')
        file_regex = re.compile(r'LISA[012345].(\d+)')
        path = Path('../data/lisa/')

        for file in listdir(path):
            if file_regex.match(file):
                lines = open(path / file, 'r').readlines() + ['Document    0']

                current_id : int = None
                current_lines : List[str] = []
                current_title : List[str] = []
                
                getting_words = False
                getting_title = False

                for line in lines:
                    match = id_regex.match(line)

                    if match is not None:
                        if len(current_lines) > 0:
                            text = ' '.join(current_lines)
                            tokens = self.TextParse(text)
                            title = ' '.join(current_title)
                            self.documents.append(Document(current_id, title, tokens, text))
                        
                        current_lines = []
                        current_title = []
                        getting_title = True
                        current_id = int(match.group(1))
                    
                    elif line.startswith('*'):
                        getting_words = False
                    elif line.isspace():
                        getting_title = False
                        getting_words = True
                    elif getting_title:
                        current_title.append(line[:-1])
                    elif getting_words:
                        current_lines.append(line[:-1])

class NPLCorpus(Corpus):
    def __init__(self):
        super().__init__(name='npl')

    def DocumentParser(self):
        id_regex = re.compile(r'(\d+)')
        lines = open('../data/npl/doc-text', 'r').readlines() + ['0']

        current_id : int = None
        current_lines : List[str] = []

        for line in lines:
            match = id_regex.match(line)

            if match is not None:
                if len(current_lines) > 0:
                    text = ' '.join(current_lines)
                    tokens = self.TextParse(text)
                    title = current_lines[0]
                    self.documents.append(Document(current_id, title, tokens, text))
                
                current_lines = []
                current_id = int(match.group(1))
            elif not line.endswith('/\n'):
                current_lines.append(line)