from django.shortcuts import render
from .models import Bid, Offer, MyCustomUser
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
from services import detail_bid_parse, bid_parser, personal_area_parse
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from api.serializers import BidSerializer, OfferSerializer, CustomUserSerializer
from rest_framework import serializers, status, generics


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyCustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all().order_by('-application_date')
    serializer_class = BidSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self):
        bid_id = self.request.get_full_path().split('/')[3]
        detail_bid_parse.save_and_return_detail_bid_json(bid_id)
        return super().get_object()



class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-validity')
    serializer_class = OfferSerializer
    lookup_field = 'number'
    # permission_classes = [permissions.IsAuthenticated]



@api_view(['GET'])
def parse_all_bid(request, *args, **kwargs) -> Response:
    """Parse or update all bids from butb/demands"""
    try:
        bid_parser.parse_bid(43)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        raise NotFound(e)


@api_view(['GET'])
def parse_all_offers(request, *args, **kwargs) -> Response:
    """Parse all offers in personal area"""
    try:
        personal_area_parse.parse_offers('905DD217-E592-4609-A9F0-6343EF70FD02',20)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def parse_offers_for_bid(request, *args, **kwargs):
    try:
        bid_id = request.GET.get('bid_id')
        print(bid_id)
        personal_area_parse.get_offers_for_bid(int(bid_id),'37BF5AA0-D976-4BAE-9B9E-67730920C5D9',50)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data='Try to update auth-token', status=status.HTTP_404_NOT_FOUND)



class BidOffersView(generics.ListAPIView):
    """Offers by bid id"""
    serializer_class = OfferSerializer


    def get_queryset(self, *args, **kwargs):
        bid_id = self.request.GET.get('bid_id')
        queryset = Offer.objects.filter(bid_id=int(bid_id))
        return queryset


@api_view(['GET', 'POST'])
def submit_an_offer(request, *args, **kwargs):
    pass


