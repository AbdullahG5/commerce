from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class bids(models.Model):
    bids=models.IntegerField(default=0,null=True)
    users=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='bids')

class Categories(models.Model):
    categories_name=models.CharField(max_length=40,default='none')
    def __str__(self):
        return self.categories_name


class auction_listings(models.Model):
    title=models.CharField(max_length=20,default="none")
    description=models.CharField(max_length=150,default="none")
    start_up_bids=models.ForeignKey(bids,on_delete=models.CASCADE,null=True,blank=True,related_name='bid')
    image = models.CharField(max_length=300,default="none")
    color=models.CharField(max_length=50,default="none")
    Brand=models.CharField(max_length=30,default="none")
    status=models.BooleanField(default=True)
    id_of_owner=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user')
    categories=models.ForeignKey(Categories,on_delete=models.CASCADE,null=True,blank=True,related_name='categories')
    watch_list=models.ManyToManyField(User,null=True,blank=True,related_name='User')
    def __str__(self) :
        return self.title
    
class comment(models.Model):
    the_comment=models.CharField(max_length=255,default="none")
    users=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='comment')
    list=models.ForeignKey(auction_listings,on_delete=models.CASCADE,null=True,blank=True,related_name='list_comment')
    def __str__(self) :
        return f"{self.the_comment} comment {self.list}"
