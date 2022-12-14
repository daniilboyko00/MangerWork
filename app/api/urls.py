from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, BidViewSet, OffersViewSet, BidOffersView,\
    parse_all_bid, parse_all_offers, parse_offers_for_bid, parse_trade_status,\
    submit_an_offer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bids', BidViewSet)
router.register(r'offers', OffersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all_bids/', parse_all_bid, name = 'all-bids'),
    path('all_offers/', parse_all_offers, name = 'all-offers'),
    # path('parse_offers_for_bid', parse_offers_for_bid, name='parse-offers-for-bid'),
    path('offers_for_bid/',BidOffersView.as_view(), name='offers_for_bid'),
    path('parse_trade_status/', parse_trade_status, name='parse-statuses'),
    path('submit_offer/', submit_an_offer, name ='submit')
]