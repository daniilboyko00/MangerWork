from django.contrib import admin
from .models import Bid



@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("purchase_order", )}




