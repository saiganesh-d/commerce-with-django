from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register, name = "register"),
    path("createListing", views.createListing, name = "createListing"),
    path("viewListing/<str:title>",views.viewListing, name = "viewListing"),
    path("close/<str:title>",views.close, name = "close"),
    path("bid/<str:title>",views.bid, name = "bid"),
    path("closed",views.closed,name = "closed"),
    path("addwatchlist/<str:title>",views.addwatchlist, name = "addwatchlist"),
    path("watchlist",views.watchlist, name = "watchlist"),
    path("deletewatchlist/<str:title>", views.deletewatchlist, name = "deletewatchlist"),
    path("categories", views.categories, name = "categories"),
    path("showcategory/<str:category>", views.showcategory , name = "showcategory")
]
