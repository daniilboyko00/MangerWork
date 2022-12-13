from django.contrib import admin
from .models import MyCustomUser, Bid, Offer


@admin.register(MyCustomUser, Bid, Offer)
class ApiAdmin(admin.ModelAdmin):
    pass
