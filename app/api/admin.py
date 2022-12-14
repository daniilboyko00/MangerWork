from django.contrib import admin
from .models import MyCustomUser, Bid, Offer, Auth_token


@admin.register(MyCustomUser, Bid, Offer, Auth_token)
class ApiAdmin(admin.ModelAdmin):
    pass
