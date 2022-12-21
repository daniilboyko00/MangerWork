from rest_framework import serializers, fields
from .models import Bid, Offer, Notification



class OfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        fields = '__all__'
        lookup_field = 'number'


class BidSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True, many=True)
    class Meta:
        model = Bid
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class NotificationSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        lookup_field = 'id'