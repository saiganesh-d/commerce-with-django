from django.contrib import admin
from .models import User,Comments,Listings,Bids,Watchlist
# Register your models here.

admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Watchlist)
