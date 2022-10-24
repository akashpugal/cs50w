from django.shortcuts import render
import markdown
import random


from . import util

def md_html(title):
    info=util.get_entry(title)
    markdowner=markdown.Markdown()
    if info==None:
        return None
    else:
        return markdowner.convert(info)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def detail(request,title):
    webb = md_html(title)
    if webb == None:
        return render(request,"encyclopedia/error.html",{
            "msg":"The requested entry does not exist"
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "info":webb
        })


def find(request):
    if request.method=="POST":
        finding=request.POST['q']
        webb=md_html(finding)
        if webb is not None:
            return render(request,"encyclopedia/entry.html",{
            "title":finding,
            "info":webb
        })
        else:
            everyEnt=util.list_entries()
            sug=[]
            for entry in everyEnt:
                if finding.lower() in entry.lower():
                    sug.append(entry)
            return render(request,"encyclopedia/search.html",{
                "sug":sug
            })



def new_page(request):
    if request.method=="GET":
        return render(request,"encyclopedia/new.html")
    else:
        title=request.POST['title']
        content=request.POST['content']
        titleExist=util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/error.html",{
                "msg":"Page you entered already exists"
            })
        else:
            util.save_entry(title,content)
            html_content=md_html(title)
            return render(request,"encyclopedia/entry.html",{
                "title":title,
                "info":html_content
                
            })

def edit(request):
    if request.method=='POST':
        title=request.POST['entry_title']
        content=util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title":title,
            "content":content
        })

def save_edit(request):
    if request.method=="POST":
        title=request.POST['title']
        info=request.POST['content']
        util.save_entry(title,info)
        html_content=md_html(title)
        return render(request,"encyclopedia/entry.html",{
                "title":title,
                "info":html_content
                
            })


def randomm(request):
    allEntries=util.list_entries()
    randomm_entry=random.choice(allEntries)
    contentt=md_html(randomm_entry)
    return render(request,"encyclopedia/entry.html",{
        "title":randomm_entry,
        "info":contentt
    })