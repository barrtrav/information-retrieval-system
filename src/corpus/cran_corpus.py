import re
from pathlib import Path
from tools import Document
from . import CorpusAnalyzer
from utils import clear_text

class CranCorpusAnalyzer(CorpusAnalyzer):
    def __init__(self, name='cran', django=False) -> None:
        super().__init__(name, django)

    def parse_documents(self):
        id_re = re.compile(r'\.I (\d+)')
        file = open(Path(f'../source/corpus/{self.name}/{self.name}.all.1400'), 'r')
        current_id = None
        current_lines = []
        current_title = []

        getting_words = False
        getting_title = False

        for i, line in enumerate(file.readlines() + ['.I 0']):
            match = id_re.match(line)
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
            elif line.startswith('.T'):
                getting_title = True
                getting_words = False
            elif line.startswith('.W'):
                getting_words = True
                getting_title = False
            elif line.startswith('.A') or line.startswith('.X'):
                getting_title = False
                getting_words = False
            elif getting_words:
                current_lines.append(line[:-1])
            elif getting_title:
                current_title.append(line[:-1])
        