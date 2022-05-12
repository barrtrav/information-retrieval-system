import re
from os import listdir
from pathlib import Path
from tools import Document
from utils import clear_text
from . import CorpusAnalyzer

class LisaCorpusAnalyzer(CorpusAnalyzer):
    def __init__(self, name='lisa') -> None:
        self.id_re = re.compile('Document\s+(\d+)')
        super().__init__(name)

    def parse_documents(self):
        corpus_path = Path(f'../source/corpus/{self.name}')
        corpus_re = re.compile(r'LISA[012345].(\d+)')
        for file in listdir(corpus_path):
            if corpus_re.match(file):
                file_path = corpus_path / file
                
                corpus_fd = open(file_path)
                current_id: int = None
                current_lines = list() 
                getting_words = False
                current_title = list() 
                getting_title = False
                
                for line in corpus_fd.readlines() + ['Document  0']:
                    match = self.id_re.match(line)
                    if match is not None:
                        if len(current_lines) > 0:
                            tokens = clear_text(" ".join(current_lines))
                            title = ' '.join(current_title).capitalize()
                            summary = '\n'.join(current_lines)
                            self.documents.append(Document(current_id, tokens, title, summary))
                        current_id = int(match.group(1))
                        current_title = []
                        current_lines = []
                        getting_title = True
                    elif line.startswith('*'):
                        getting_words = False
                    elif line.isspace():
                        getting_title = False
                        getting_words = True
                    elif getting_title:
                        current_title.append(line[:-1])
                    elif getting_words:
                        current_lines.append(line[:-1])