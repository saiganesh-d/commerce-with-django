from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


#class to keep track of listings
class Listings(models.Model):
    title = models.CharField(max_length = 64, unique = True)
    price = models.IntegerField(default = 0)
    description = models.TextField(max_length = 500)
    category = models.CharField(max_length = 64,blank = True)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    owner = models.CharField(max_length = 64 , default = 'SOME STRING')
    status = models.BooleanField(default = True)
    winner = models.CharField(max_length = 64 , blank = True)

    def __str__(self):
        return f"{self.title}, {self.price},{self.description},{self.category},{self.image},{self.owner},{self.status},{self.winner}"


#class to keep track of the comments
class Comments(models.Model):
    username = models.CharField(max_length = 64)
    comment = models.TextField(max_length = 500 , blank = False)
    listing = models.ForeignKey(Listings,on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.username}, {self.comment}, {self.listing}"


#class to keep track of biddings
class Bids(models.Model):
    username = models.CharField(max_length = 64)
    listing = models.ForeignKey(Listings,on_delete = models.CASCADE)
    bid = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.username},{self.listing},{self.bid}"


#user Watchlist databse track
class Watchlist(models.Model):
    username = models.CharField(max_length = 64)
    listing = models.ForeignKey(Listings,on_delete = models.CASCADE,related_name = "listing")

    def get_title(self):
        return self.listing.title

    def __str__(self):
        return f"{self.username},{self.listing}"
