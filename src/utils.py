import math
from typing import List
from nltk.corpus import stopwords
from color import *

STOPWORDS = ' | '.join([x for x in stopwords.words('english')])
REGEX = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'

class Document:
    def __init__(self, id : int, title : str, tokens : List[str], text : str) -> None:
        self.id = id
        self.title = title
        self.tokens = tokens
        self.text = text[0].upper() + text[1:]
        self.summary = self.text[:200] + '...'
    
    def __str__(self) -> str:
        return f'{GREEN}{self.id}{RESET} : {self.title}'
    
    def __repr__(self) -> str:
        return str(self)