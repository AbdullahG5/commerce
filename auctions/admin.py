from django.contrib import admin
from .models import User ,Categories,auction_listings,comment,bids

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(auction_listings)
admin.site.register(comment)
admin.site.register(bids)

# Register your models here.
