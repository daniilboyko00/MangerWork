from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Bid 
from django.http import HttpResponse, JsonResponse
from services import detail_bid_parse
from django.db.models import Q

# Create your views here.

class BidListView(ListView):
    model = Bid
    template_name = 'index.html'
    # context_object_name = 'all_bids'
    paginate_by = 10


    def get_queryset(self): # новый
        if self.request.user.is_authenticated:
            print('q123')
        query = self.request.GET.get('q')
        object_list = Bid.objects.all()
        if query:
            self.paginate_by = 100
            object_list = Bid.objects.filter(
                Q(procurement_name__icontains=query)
            )
            print(len(object_list))
            return object_list
        return object_list



class BidDetailView(DetailView):
    model = Bid
    slug_field = 'purchase_order'
    template_name = 'index.html'


    def get(self,request, *args, **kwargs):
        id = int(self.request.get_full_path().split('/')[2])
        resp = detail_bid_parse.save_and_return_detail_bid_json(id)
        return JsonResponse(resp, safe=False, json_dumps_params={'ensure_ascii': False})
