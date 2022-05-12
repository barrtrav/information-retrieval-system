from tools import Document, Token
from sqlite3 import connect, Connection

def create_database(db_path):
    db = connect(db_path)
    db.execute('CREATE TABLE IF NOT EXISTS "index_document" ("id" integer NOT NULL PRIMARY KEY, "lexer" text NOT NULL, "title" text NOT NULL, "text" text NOT NULL);')
    db.execute('CREATE TABLE IF NOT EXISTS "index_token" ("lexer" varchar(20) NOT NULL PRIMARY KEY, "documents" text NOT NULL, "frequency" text NOT NULL, "max_freq" integer NOT NULL);')
    db.execute('CREATE TABLE IF NOT EXISTS "index_ratings" ("id" integer NOT NULL PRIMARY KEY, "value" integer NOT NULL);')
    return db

def add_document(db:Connection, doc:Document):
    lexer = ' '.join([lex for lex in doc.lexer])
    db.execute(f'INSERT INTO "index_document" ("id", "lexer", "title", "text") values ({doc.id}, "{lexer}", "{doc.title}", "{doc.text}");')

def add_token(db:Connection, token:Token):
    documents = ''
    frequency = ''
    for doc_id in token.documents:
        documents += str(doc_id) + ' '
        frequency += str(token.documents[doc_id]) + ' '
    db.execute(f'INSERT INTO "index_token" ("lexer", "documents", "frequency", "max_freq") values ("{token.lexer}", "{documents}", "{frequency}", {token.max});')