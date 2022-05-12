from posixpath import split
import sqlite3 as sq

from database import *
from pathlib import Path
from tools import TokenList, Document, Token

class CorpusAnalyzer:
    def __init__(self, name='corpus' , django=False) -> None:
        self.name = name
        self.documents = list()
        self.index = TokenList()
        try:
            if django: self.load_dj_database()
            else: self.load_database()
        except FileNotFoundError:
            self.parse_documents()
            self.parse_index()
            self.save_database()
        self.mapping = {doc.id:doc for doc in self.documents}
    
    def parse_documents(self):
        raise NotImplementedError

    def parse_index(self):
        for doc in self.documents:
            for lex in doc.lexer:
                self.index.add(lex, doc.id)

    def load_dj_database(self):
        from index.models import IndexDocument, IndexToken
        
        docuemtns = IndexDocument.objects.using(self.name).all()
        tokens = IndexToken.objects.using(self.name).all()

        for doc in docuemtns:
            self.documents.append(Document(doc.id, doc.lexer.split(' '), doc.title, doc.text))
        
        for tok in tokens:
            token = Token(tok.lexer)
            token.documents = { int(doc_id):int(freq) for doc_id, freq in zip(tok.documents.split(' '), tok.frequency.split())}
            token.max = tok.max_freq
            self.index.tokens[tok.lexer] = token

    def load_database(self):
        db_path = Path(f'../source/database/{self.name}.db')
        if not db_path.exists(): raise FileNotFoundError
        
        db = sq.connect(db_path)
        cursor = db.cursor()
        
        for id, lexer, title, text in cursor.execute('SELECT * FROM "index_document";'):
            self.documents.append(Document(id, lexer.split(' '), title, text))
        
        for lexer, documents, frequency, max_freq in cursor.execute('SELECT * FROM "index_token";'):
            token = Token(lexer)
            token.documents = { int(doc_id):int(freq) for doc_id, freq in zip(documents.split(' '), frequency.split())}
            token.max = max_freq
            self.index.tokens[lexer] = token

        db.close()
        
    def save_database(self):
        db_path = Path(f'../source/database/{self.name}.db')
        if db_path.exists(): raise FileExistsError

        db = create_database(db_path)

        for doc in self.documents:
            add_document(db, doc)
        for lex in self.index.tokens:
            add_token(db, self.index.tokens[lex])
        
        db.commit()
        db.close()