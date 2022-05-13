class Document:
    def __init__(self, id, lexer, title, text) -> None:
        self.id = id
        self.text = text
        self.title = title
        self.lexer = lexer

    def __str__(self) -> str:
        return f'{self.id}: {self.title}'

    def __repr__(self) -> str:
        return str(self)

    @property
    def get_summary(self):
        return self.text.capitalize()[:200] + '...'

class Token:
    def __init__(self, lexer:str) -> None:
        self.max = 0
        self.lexer = lexer
        self.documents = dict()

    def __str__(self) -> str:
        return f'{self.lexer} : {[id for id in self.documents]}'
    
    def __repr__(self) -> str:
        return str(self)

    def add_doc(self, doc:int) -> None:
        try:
            self.documents[doc] += 1
        except KeyError:
            self.documents[doc] = 1
        
        self.max = max(self.max, self.documents[doc])
        return self

    def tf(self, doc:int) -> float:
        try:
            return self.documents[doc] / self.max
        except KeyError:
            return 0
    
    @property
    def ni(self) -> int:
        ni = len(self.documents)
        return ni if ni else 1

class TokenList:
    def __init__(self) -> None:
        self.tokens = dict()

    def add(self, lexer:str, doc:Document) -> None:
        try:
            self.tokens[lexer].add_doc(doc)
        except KeyError:
            self.tokens[lexer] = Token(lexer).add_doc(doc)

    def get(self, lexer:str) -> Token:
        try:
            return self.tokens[lexer]
        except KeyError:
            return Token(lexer)