from rest_framework import serializers, fields
from .models import Bid, Offer, MyCustomUser


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class OfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        fields = '__all__'
        lookup_field = 'number'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCustomUser
        fields = ['email','full_name']
