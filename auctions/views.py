from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import auction_listings,Categories,User,comment,bids


def index(request):
    active_list=auction_listings.objects.filter(status=True)
    all_categories=Categories.objects.all() 
    return render(request, "auctions/index.html",{
        'auction_listings':active_list,
        'Categories': all_categories
    })


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
    
def creat_listing(request):
    if request.method == "GET":
        all_categories=Categories.objects.all()
        return render(request,"auctions/creat_listing.html",{
            'Categories':all_categories
        })
    if request.method == "POST":
        title=request.POST['title']
        description=request.POST['description']
        start_up_bids=request.POST['start_up_bids']
        image=request.POST['image']
        color=request.POST['color']
        id_of_owner=request.user
        category=request.POST['Categories']
        Brand=request.POST['Brand']
        Categories_type=Categories.objects.get(categories_name=category)
        Bids=bids(bids=int(start_up_bids), users=id_of_owner)
        Bids.save()
        list=auction_listings(title=title,description=description,start_up_bids=Bids,color=color,Brand=Brand,image=image,id_of_owner=id_of_owner,categories=Categories_type)
        list.save()
        active_list=auction_listings.objects.filter(status=True)
        return render(request, "auctions/index.html",{
            'auction_listings':active_list,
            'Categories': all_categories})
    
def watch_list(request):
    the_user=request.user
    listing=the_user.User.all()
    return render(request,'auctions/watch_list.html',{
        'auction_listings':listing
    })
    
def display_categories(request):
    if request.method=='POST':
        Category_data=request.POST['Category']
        Category=Categories.objects.get(categories_name=Category_data)
        active_list=auction_listings.objects.filter(status=True,categories=Category)
        all_categories=Categories.objects.all() 
        return render(request, "auctions/index.html",{
            'Categories': all_categories,
            'auction_listings':active_list,
        })
def listing(request,id):
    list_data=auction_listings.objects.get(pk=id)
    is_in_watchlist=request.user in list_data.watch_list.all() 
    all_comments=comment.objects.filter(list=list_data)
    the_owner=request.user.username == list_data.id_of_owner.username
    return render(request,"auctions/listing.html",{
        'auction_listings':list_data,
        'ckeck_in':is_in_watchlist,
        'all_comments':all_comments,
        'the_owner':the_owner,
        })

def addW(request,id):
    list_data=auction_listings.objects.get(pk=id)
    the_user=request.user
    list_data.watch_list.add(the_user)
    return HttpResponseRedirect(reverse('listing',args=(id, )))

def removeW(request,id):
    list_data=auction_listings.objects.get(pk=id)
    the_user=request.user
    list_data.watch_list.remove(the_user)
    return HttpResponseRedirect(reverse('listing',args=(id, )))

def comments(request,id):
    user=request.user
    list_data=auction_listings.objects.get(pk=id)
    comments=request.POST['newcomment']
    new_comment=comment(users=user,list=list_data,the_comment=comments)
    new_comment.save()
    return HttpResponseRedirect(reverse('listing',args=(id, )))
def Bid(request,id):
    if request.method == "POST":
        newbids=request.POST['newbids']
        listing_data=auction_listings.objects.get(pk=id)
        is_in_watchlist=request.user in listing_data.watch_list.all() 
        all_comments=comment.objects.filter(list=listing_data)
        the_owner=request.user.username == listing_data.id_of_owner.username
    if int(newbids) > listing_data.start_up_bids.bids:
        update_bid=bids(users=request.user,bids=int(newbids))
        update_bid.save()
        listing_data.start_up_bids=update_bid
        listing_data.save()
        return render(request,"auctions/listing.html",{
            'auction_listings':listing_data,
            'update':True,
            'do':'run',
            'ckeck_in':is_in_watchlist,
            'all_comments':all_comments,
            'the_owner':the_owner,
            'do_0':'Well done!',
            'do_1':'Aww yeah, you successfully bid on this item',
            'do_2':'Thank you',

        })
    else:
        return render(request,"auctions/listing.html",{
            'auction_listings':listing_data,
            'update':False,
            'do':'run',
            'ckeck_in':is_in_watchlist,
            'all_comments':all_comments,
            'the_owner':the_owner,
        })

def close(request,id):
    list_data=auction_listings.objects.get(pk=id)
    list_data.status=False
    is_in_watchlist=request.user in list_data.watch_list.all() 
    all_comments=comment.objects.filter(list=list_data)
    the_owner=request.user.username == list_data.id_of_owner.username
    list_data.save()
    return render(request,"auctions/listing.html",{
        'auction_listings':list_data,
        'ckeck_in':is_in_watchlist,
        'all_comments':all_comments,
        'the_owner':the_owner,
        'update':True,
        'do':'run',
        'do_0':'Congratulations, you auction is close',
        'update':True,
        })








        
    
