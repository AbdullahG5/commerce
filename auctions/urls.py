from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creat_listing",views.creat_listing, name="C_L"),
    path("display_categories",views.display_categories,name="DP_C"),
    path("watch_list",views.watch_list,name="W_L"),
    path("listing/<int:id>",views.listing,name='listing'),
    path("addW/<int:id>",views.addW,name='addW'),
    path("removeW/<int:id>",views.removeW,name='removeW'),
    path("comments/<int:id>",views.comments,name='A_C'),
    path("bids/<int:id>",views.Bid,name='bids'),
    path("close/<int:id>",views.close,name='close'),
]
