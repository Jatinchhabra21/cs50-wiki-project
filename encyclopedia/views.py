from django.shortcuts import render
from markdown2 import markdown,Markdown
from . import util
from django.http import HttpResponse,HttpResponseRedirect
from random import shuffle
from django import forms 
from django.urls import reverse


class SearchForm(forms.Form):
    search = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

class NewEntryForm(forms.Form):
    title = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Title'}))
    content = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder':'Write content here'}))


def index(request):
    res = []
    query = ""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            for title in util.list_entries():
                if query.lower() == title.lower():
                    return display_entry(request,title)
                if query.lower() in title.lower():
                    res.append(title)
                
                if res!=[]:
                    
                    return render(request,"encyclopedia/search.html",{
                        'results':res,
                        'query':query,
                        "form":SearchForm()
                    })
            else:
                return render(request,"encyclopedia/index.html",{
                    "entries":util.list_entries(),
                    "form":SearchForm()
                })

        return HttpResponse(f"{query}")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form':SearchForm()
    })

def display_entry(request,title):
    entryPage = util.get_entry(title)
    if entryPage is None:
        return render(request,"encyclopedia/nonExistingEntry.html",{
            'title':title,
            'form':SearchForm()
        })
    else:
        markdowner = Markdown()
        return render(request,"encyclopedia/entry.html",{
            'entry':markdowner.convert(entryPage),
            'title':title,
            'form':SearchForm()
        })

def display_random(request):
    entry_list = util.list_entries()
    shuffle(entry_list)
    return display_entry(request, entry_list[0])

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["title"] in util.list_entries():
                return render(request,'encyclopedia/EntryExists.html',{
                'form':SearchForm()
                })
            else:
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse(f'display_entry',args=(title,)))
    return render(request,'encyclopedia/newEntry.html',{
        'Entryform':NewEntryForm(),
        'form':SearchForm()
    })

def edit_entry(request,title):

    if request.method == "POST":
        util.save_entry(title, request.POST["content"])
        return HttpResponseRedirect(reverse('display_entry',args=(title,)))
    return render(request,"encyclopedia/edit.html",{
        'title':title,
        'content':util.get_entry(title),
        'form':SearchForm()
    })
    

    