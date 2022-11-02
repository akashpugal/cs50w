from email import message
from email.policy import default
from tokenize import blank_re
from django.contrib.auth.models import AbstractUser
from django.db import models
from auctions.views import catalogue


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName=models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName
    

class Bid(models.Model):
    bid=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userBid")

  


class Catalogue(models.Model):
    headingg=models.CharField(max_length=30)
    note=models.CharField(max_length=300)
    picLink=models.CharField(max_length=1000)
    price=models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name="category")
    Watchlist=models.ManyToManyField(User,blank=True,null=True,related_name="CatalogueWatchlist")

    def __str__(self):
        return self.headingg


class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userComments")
    catalogue=models.ForeignKey(Catalogue,on_delete=models.CASCADE,blank=True,null=True,related_name="catalogueComments")
    message=models.CharField(max_length=200)

    def _str_(self):
        return f"{self.author} comment on {self.catalogue}" 
        


    
    