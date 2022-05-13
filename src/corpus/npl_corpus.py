import re
from pathlib import Path
from tools import Document
from . import CorpusAnalyzer
from utils import clear_text

class NplCorpusAnalyzer(CorpusAnalyzer):
    def __init__(self, name='npl', django=False) -> None:
        super().__init__(name, django)

    def parse_documents(self):
        file = open(Path(f'../source/corpus/{self.name}/doc-text'), 'r')
        id_re = re.compile(r'(\d+)')
        current_id = None
        current_lines = []

        for line in file.readlines() + [' 0 ']:
            match = id_re.match(line)
            if match is not None:
                if len(current_lines) > 0:
                    tokens = clear_text(" ".join(current_lines))
                    title = f'Document No.{current_id}'
                    summary = '\n'.join(current_lines)
                    self.documents.append(Document(current_id, tokens, title, summary))
                current_id = int(match.group(1))
                current_lines = []
            elif not line.endswith('/\n'):
                current_lines.append(line[:-1])