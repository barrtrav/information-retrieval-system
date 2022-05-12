import os

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from corpus import CorpusAnalyzer
from models import VectorMRI
from system import IRSystem

try:
    db_name = os.environ['database']
    analyzer = CorpusAnalyzer(name=db_name, django=True)
    system = IRSystem(VectorMRI(analyzer), django=True)
except KeyError:
    system = None

urlpatterns = []

def index(request):
    query = request.GET.get('query')
    
    if query:
        #analyzer = system.parse
        docs = system.make_query(query)
        query = query[:50]+'...'
    else:
        docs = []

    return render(request, 'index.html', context={'query':query, 'docs': docs[:20]})

def viewdoc(request):
    doc_id = int(request.get_full_path().split('/')[-1])
    doc = analyzer.mapping[doc_id]
    return render(request, 'document.html', 
        context={
            'id':str(doc.id) + ' - ' + doc.title[:20], 
            'title':doc.title, 
            'text':doc.text.capitalize()}
        )