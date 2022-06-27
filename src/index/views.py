from django.shortcuts import render, redirect
from django.http import HttpResponse

from model import *
from corpus import *
from system import *
from expansion import Expansion

systems = VectorSystem(VectorModel(CranCorpus()))
user_feed = []
last_query = []
last_docs = []

def home(request):
    query = request.GET.get('query')
    if query  is not None:return render(request, 'index.html', context = MakeQuery(query))
    return render(request, 'home.html')

def document(request, doc_id):
    user_feed.append(doc_id)
    doc = systems.model.corpus.documents[doc_id]
    return render(request, 'document.html', context={'doc' : doc})

def MakeQuery(query):
    
    if last_query and user_feed:
        systems.UserFeedBack(last_query[-1], user_feed, last_docs)
        while len(last_docs) > 0:
            last_docs.pop(0)
        while len(user_feed) > 0:
            user_feed.pop(0)
        while len(last_query) > 0:
            last_query.pop(0)

    docs = []
    recommend = []
    expansion = []

    if query:
        docs, ranking = systems.MakeQuery(query)
        systems.AutoFeedBack(query, ranking)
        expansion = Expansion(query, systems.model)
        recommend = systems.Recommend(ranking)

        for doc_id, _ in ranking:
            last_docs.append(doc_id)
        last_query.append(query)
    
    return {'docs' : docs, 'recommend' : recommend, 'expansion' : expansion}