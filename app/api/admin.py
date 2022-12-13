from django.contrib import admin
from .models import MyCustomUser, Bid, Offer, Auth_token, Arhive


@admin.register(MyCustomUser, Bid, Offer, Auth_token, Arhive)
class ApiAdmin(admin.ModelAdmin):
    pass
