import re

regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'

def stopwords(language:str='english') -> str:
    try:
        words = open(f'../source/stopwords/{language}', 'r').read()
        words = re.sub('\s+', ' ', words)
        words = ' | '.join([x for x in words.split(sep=' ')])
    except:
        print(f'Language {language} not exist.')
        words = ''

    return words[:-2]

def clear_text(text) -> list:
    new_text = text.lower()
    new_text = re.sub(regex, ' ', new_text)
    new_text = re.sub('\d+', ' ', new_text)
    new_text = re.sub('\s+', ' ', new_text)
    new_text = re.sub(stopwords(), ' ', new_text)

    return [lex for lex in new_text.split(sep=' ')]

def query_parse(text:str) -> tuple:
    max_freq = 0
    query = dict()
    for lex in clear_text(text):
        try:
            query[lex] += 1
        except KeyError:
            query[lex] = 1
        max_freq = max(max_freq, query[lex])
    
    return query, max_freq
