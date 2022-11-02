from tkinter.tix import NoteBook
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


#from .models import User,Category,Catalogue,Comment

import auctions.models

def index(request):
    activeCatalogues = auctions.models.Catalogue.objects.filter(isActive=True)
    allCategories = auctions.models.Category.objects.all()
    return render(request, "auctions/index.html",{
        "catalogues":activeCatalogues,
        "categories":allCategories
    })


def createCatalogue(request):
    if request.method=="GET":
        allCategories=auctions.models.Category.objects.all()
        return render(request,"auctions/create.html",{
            "categories":allCategories
        })
    else:
        headingg=request.POST['headingg']
        note=request.POST['note']
        picLink=request.POST['picLink']
        price=request.POST['price']
        category=request.POST['category']
        currentUser=request.user
        categoryData=auctions.models.Category.objects.get(categoryName=category)
        bid=auctions.models.Bid(bid=int(price), user=currentUser)
        bid.save()
        newCatalogue=auctions.models.Catalogue(
            headingg=headingg,
            note=note,
            picLink=picLink,
            price=bid,
            category=categoryData,
            owner=currentUser
        )
        newCatalogue.save()
        return HttpResponseRedirect(reverse(index))






def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = auctions.models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def displayCategory(request):
    if request.method=="POST":
        categoryFromForm=request.POST['category']
        category=auctions.models.Category.objects.get(categoryName=categoryFromForm)
        activeCatalogues=auctions.models.Catalogue.objects.filter(isActive=True,category=category)
        allCategories=auctions.models.Category.objects.all()
        return render(request, "auctions/index.html",{
            "catalogues":activeCatalogues,
            "categories":allCategories
        })



def catalogue(request,id):
    catalogueData=auctions.models.Catalogue.objects.get(pk=id)
    isCatalogueInWatchlist=request.user in catalogueData.Watchlist.all()
    allComments=auctions.models.Comment.objects.filter(catalogue=catalogueData)
    isOwner=request.user.username==catalogueData.owner.username
    return render(request,"auctions/catalogue.html",{
        "catalogue":catalogueData,
        "isCatalogueInWatchlist":isCatalogueInWatchlist,
        "allComments":allComments,
        "isOwner":isOwner
    })


def closeAuction(request,id):
    catalogueData=auctions.models.Catalogue.objects.get(pk=id)
    catalogueData.isActive=False
    catalogueData.save()
    isOwner=request.user.username==catalogueData.owner.username
    isCatalogueInWatchlist=request.user in catalogueData.Watchlist.all()
    allComments=auctions.models.Comment.objects.filter(catalogue=catalogueData)
    return render(request,"auctions/catalogue.html",{
        "catalogue":catalogueData,
        "isCatalogueInWatchlist":isCatalogueInWatchlist,
        "allComments":allComments,
        "isOwner":isOwner,
        "update":True,
        "message":"Congratulations! Your auction is closed"
    })


def removeWatchlist(request,id):
    catalogueData=auctions.models.Catalogue.objects.get(pk=id)
    currentUser=request.user
    catalogueData.Watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("catalogue",args=(id, )))



def addWatchlist(request,id):
    catalogueData=auctions.models.Catalogue.objects.get(pk=id)
    currentUser=request.user
    catalogueData.Watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("catalogue", args=(id, )))


def displayWatchlist(request):
    currentUser=request.user
    catalogues=currentUser.CatalogueWatchlist.all()
    return render(request,"auctions/watchlist.html",{
        "catalogues":catalogues
    })


def addComment(request,id):
    currentUser=request.user
    catalogueData=auctions.models.Catalogue.objects.get(pk=id)
    message=request.POST['newComment']
    newComment=auctions.models.Comment(
        author=currentUser,
        catalogue=catalogueData,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("catalogue",args=(id, )))


def addBid(request,id):
    newBid=request.POST['newBid']
    catalogueData=auctions.models.Catalogue.objects.get(pk=id)
    isCatalogueInWatchlist=request.user in catalogueData.Watchlist.all()
    allComments=auctions.models.Comment.objects.filter(catalogue=catalogueData)
    isOwner=request.user.username==catalogueData.owner.username
    if int(newBid)>catalogueData.price.bid:
        updateBid=auctions.models.Bid(user=request.user,bid=int(newBid))
        updateBid.save()
        catalogueData.price=updateBid
        catalogueData.save()
        return render(request,"auctions/catalogue.html",{
            "catalogue":catalogueData,
            "message":"Bid was updated successfully",
            "update":True,
            "isCatalogueInWatchlist":isCatalogueInWatchlist,
            "allComments":allComments,
            "isOwner":isOwner
        })
    else:
        return render(request,"auctions/catalogue.html",{
            "catalogue":catalogueData,
            "message":"Bid updation failed",
            "update":False,
            "isCatalogueInWatchlist":isCatalogueInWatchlist,
            "allComments":allComments,
            "isOwner":isOwner
        })

    