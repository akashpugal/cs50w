from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
#def index(request):
#    return render(request,"helloo/index.html")

def brain(request):
    return HttpResponse("Hello Brain")

def david(request):
    return HttpResponse("Hello David")

def greet(request, name):
    return render(request, "helloo/greet.html",{
        "name" : name.capitalize()
    })