from django.shortcuts import render, redirect
from .models import *
from .forms import DocumentForm
from main.models import *

def documents(request):
    documents = Document.objects.all()
    parties = Party.objects.all()
    headlines = Headline.objects.all()



    context = {'documents': documents, 'parties': parties, 'headlines': headlines,}
    return render(request, 'document/documents.html', context)

def document(request,pk):
    document = Document.objects.get(id=pk)
    documents = Document.objects.all()
    parties = Party.objects.all()
    headlines = Headline.objects.all()
    
    context = {'document': document, 'documents': documents, 'parties': parties, 'headlines': headlines,}
    return render(request, 'document/document.html', context)

def create_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('documents')
    else:
        form = DocumentForm()
    return render(request, 'document/create_document.html', {'form': form})


