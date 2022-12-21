from django.contrib import admin
from .models import Bid, Offer


@admin.register( Bid, Offer)
class ApiAdmin(admin.ModelAdmin):
    pass
