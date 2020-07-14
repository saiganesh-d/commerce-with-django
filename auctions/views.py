from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User,Comments,Listings,Bids,Watchlist

#@login_required(login_url="/login", redirect_field_name='')index View of the site
def index(request):
    if request.user.is_authenticated:
        listings = Listings.objects.filter(status = True)
        return render(request, "auctions/index.html",{"listings":listings,"check": True})

    return render(request, "auctions/message.html",{"message": "Login Required."})

#login function
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

#logout Fucntion
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#user register Function
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#function When user request for create Listings
def createListing(request):
    if request.method == "GET":
        return render(request,"auctions/listing.html")

    # if the request method is POST
    title = request.POST.get("title")
    alldata = Listings.objects.all()
    for data in alldata:
        if data.title == title:
            return render(request,"auctions/message.html",{"message": "Sorry, Title Must Be Unique."})
    price = int( request.POST.get("price"))
    description = request.POST.get("description")
    image = request.POST.get("image")
    category = request.POST.get("category")
    username = request.user.username
    #Adding Data to DATABASE
    add = Listings(title = title,price = price,description = description,
        image = image ,category = category,owner = username,status = True)
    add.save()
    #collecting All data
    list = Listings.objects.all()
    return render(request,"auctions/viewlist.html" ,{"list":list})


#View Perticular listing Funciton
def viewListing(request,title):
    list = Listings.objects.get(title = title)
    if request.method == "GET":
        if list.status == True:
            bids = Bids.objects.filter(listing = list)
            comment = Comments.objects.filter(listing = list)
            if comment:
                return render(request,"auctions/viewlist.html",{"list":list,"bids":bids,"comments":comment})
            return render(request,"auctions/viewlist.html",{"list":list,"bids":bids})
        return render(request,"auctions/closedlisting.html",{"list":list})

    #if Method is POST means comment added request made
    comment = request.POST.get("comment")
    add_comment = Comments(username = request.user.username,comment = comment,listing = list)
    add_comment.save()
    return render(request,"auctions/message.html",{"message": "Comment Added!"})




#Function to close Listing
def close(request,title):
    list = Listings.objects.get(title = title)
    list.status = False
    highBid = Bids.objects.all().aggregate(max_bid=(Max("bid")))
    bider = Bids.objects.get(bid = highBid['max_bid'])
    list.winner = bider.username
    list.save()
    return render(request,"auctions/message.html",{"message": "Listing Has Been closed!"})


#when user request to bid on a perticular Title
def bid(request,title):
    listing = Listings.objects.get(title = title)
    price = int(float(request.POST.get("bid")))
    if price < listing.price:
        return render(request,"auctions/message.html",{"message": "Bid Must be Greater then current price."})

    #if bid value is valid
    listing.price = price
    listing.save()
    username = request.user.username
    bid = Bids(username = username,listing = listing,bid = price )
    bid.save()
    return render(request,"auctions/message.html",{"message": "Your bid Has been Placed."})


#function to display all the closed listings
def closed(request):
    listing = Listings.objects.filter(status = False)
    return render(request, "auctions/index.html" ,{"listings":listing, "check": False})


#user Requested to view Watchlist
def watchlist(request):
    username = request.user.username
    ids = []
    selected = []
    listings = Watchlist.objects.values_list('listing',flat = True).filter(username = username)
    for i in listings:
        ids.append(i)

    for j in ids:
        list = Listings.objects.get(pk = j)
        selected.append(list)
    return render(request, "auctions/watchlist.html" ,{"lists":selected})


#user requested to add list in a watchlist
def addwatchlist(request,title):
    listing = Listings.objects.get(title = title)
    username = request.user.username
    listings = Watchlist.objects.values_list('listing',flat = True).filter(username = username)
    for i in listings:
        if listing.id == i:
            return render(request, "auctions/message.html",{"message": "Already added to Watchlist!"})
    watchlist = Watchlist(username = username , listing = listing)
    watchlist.save()
    return render(request,"auctions/message.html",{"message": "Added to Watchlist."})


#Remove an item from the Watchlist
def deletewatchlist(request, title):
    username = request.user.username
    list = Listings.objects.get(title = title)
    toDeleteList = Watchlist.objects.get(username = username, listing_id = list.id).delete()
    return render(request,"auctions/message.html",{"message": "Deleted from Watchlist!"})


#when user request to see catagory page
def categories(request):
    categories_ = []
    allLists = Listings.objects.all()
    for i in allLists:
        if i.category not in categories_:
            categories_.append(i.category)

    return render(request,"auctions/categories.html",{"categories": categories_})


#Show Listings of a perticular category
def showcategory(request, category):
    allLists = Listings.objects.all()
    selectedLists = []
    for i in allLists:
        if i.category == category:
            selectedLists.append(i)

    return render(request,"auctions/index.html",{"listings":selectedLists})
