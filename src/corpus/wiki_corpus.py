import re
from pathlib import Path
from tools import Document
from . import CorpusAnalyzer
from utils import clear_text
import json

class WikiCorpusAnalyzer(CorpusAnalyzer):
    def __init__(self, name='wiki', django=False) -> None:
        super().__init__(name, django)

    def parse_documents(self):
        docs = json.load(open(Path(f'../source/corpus/{self.name}_docs.json'), 'r', encoding='utf-8'))
        for id, (title, text) in enumerate(docs.items()):
            tokens = clear_text(text)
            self.documents.append(Document(id, tokens, title, text))