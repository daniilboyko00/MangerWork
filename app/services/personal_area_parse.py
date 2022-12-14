import requests
import os
import django
from django.db.utils import IntegrityError
from django.utils import timezone
import sys
sys.path.append(r"D:\MangerWork\app")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from api.models import Offer, Bid
from dateutil import parser



def parse_status_of_trades(token,pages):
    cookies = {
    'session-cookie': '1730597102a006174148f3bcbeb261f5bb9fda7a3b13720d446e24a3eb4d82c71ec6c71f3733a3f12a36a7d6952eca14',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'session-cookie=1730597102a006174148f3bcbeb261f5bb9fda7a3b13720d446e24a3eb4d82c71ec6c71f3733a3f12a36a7d6952eca14',
        'Origin': 'https://ppt.butb.by',
        'Referer': 'https://ppt.butb.by/ppt-new/profile/bids/downwardExpirationDate',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-auth-token': '{'+f'{token}'+'}',
        'x-language': 'ru',
    }
    for i in range(pages):
        json_data = {
        'typeTrade': 4,
        'mainFilters': {
            'roleInTrade': 3,
            'tradeStatusCode': None,
        },
        'searchFilters': {
            'searchString': None,
            'productName': None,
            'fabricator': None,
            'regNum': None,
            'description': None,
            'tnvedCode': None,
        },
        'paginationFilters': {
            'page': i,
            'pageSize': 50,
        },
    }
        response = requests.post('https://ppt.butb.by/PPT-Rest/api/trades', cookies=cookies, headers=headers, json=json_data)
        for j in range(len(response.json()['list'])):
            trade_json = response.json()['list'][j]
            Bid.objects.filter(purchase_order = int(trade_json['id'])).update(
                trade_status = int(trade_json['tradeStatus']['code']),
                trade_status_message = trade_json['tradeStatus']['message']
            )
            try:
                bid = Bid.objects.get(purchase_order=int(trade_json['id']))
            except Bid.DoesNotExist:
                new_bid = Bid(
                    purchase_order = int(trade_json['id']),
                    application_date =  None,
                    application_validity_period = None,
                    procurement_name = trade_json['productname'],
                    product_information = None,
                    brand = None,
                    buyer_country = trade_json['country'],
                    qntunits = trade_json['qntunits'],
                    producing_country = None,
                    terms_of_payment = None,
                    delivery_conditions = None,
                    delivery_time = None,
                    exposure_time =  None,
                    application_is_bidding = trade_json['attrTradings']['name'],
                    price = trade_json['price'],
                    number_of_goods = trade_json['quantity'],
                    cost = trade_json['fullCost'],
                    currency = trade_json['currency'],
                    technical_documentation_file_name = None,
                    application_link = f"https://ppt.butb.by/ppt-new/catalog-demands/order/{trade_json['id']}",
                    scraping_date = timezone.now(),
                    slug = int(trade_json['id']),
                    tnvedcode = None,
                    number_of_subcount = trade_json.get('viewSubcount') if trade_json.get('viewSubcount') else None,
                    subcount_link = None
                    )
                new_bid.save()
                bid = Bid.objects.get(purchase_order=int(trade_json['id']))
            if trade_json.get('offers'):
                for offer in trade_json['offers']:
                    try:
                        offer_obj = Offer.objects.get(number=int(offer['id']))
                    except Offer.DoesNotExist:
                        continue
                    Offer.objects.filter(number=int(offer['id'])).update(
                        status_in_trade = offer['statusDescription']
                    )
                    bid.offer.add(offer_obj)
        if response.json()['list'] == []:
            break




def parse_offers(token: str ,pages: int):
    cookies = {
        'session-cookie': '1730000c9cd8ab834148f3bcbeb261f54562d4ac0d03074ae80fe13e8a5569d552439deb96928510d3516b2837008b77',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'session-cookie=1730000c9cd8ab834148f3bcbeb261f54562d4ac0d03074ae80fe13e8a5569d552439deb96928510d3516b2837008b77',
        'Origin': 'https://ppt.butb.by',
        'Referer': 'https://ppt.butb.by/ppt-new/profile/my-orders-sell/active',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-auth-token': '{'+f'{token}'+'}',
        'x-language': 'ru',
    }
    for i in range(pages):
        json_data = {
            'status': 2,
            'mainFilters': {
                'typeTrade': {
                    'rise': False,
                    'simple': False,
                },
                'statusDemand': {
                    'open': False,
                    'close': False,
                },
                'tradingDate': None,
                'validity': None,
                'currency': None,
                'vatRate': [],
                'price': [
                    None,
                    None,
                ],
                'payment': {
                    'upon': False,
                    'reg': False,
                },
                'delivery': None,
                'sellerCntry': None,
                'productCntry': None,
                'locationCntry': None,
            },
            'searchFilters': {
                'searchString': None,
                'productName': None,
                'fabricator': None,
                'regNum': None,
                'description': None,
                'tnvedCode': None,
            },
            'paginationFilters': {
                'page': i,
                'pageSize': 100,
            },
        }
        response = requests.post('https://ppt.butb.by/PPT-Rest/api/offers/own', cookies=cookies, headers=headers, json=json_data)
        try:
            for j in range(len(response.json()['list'])):
                offer_json = response.json()['list'][j]
                try:
                    offer = Offer(
                        number = int(offer_json['id']),
                        product_name = offer_json['productname'],
                        country = offer_json['country'],
                        price = float(offer_json['price']) ,
                        currency = offer_json['currency'] ,
                        full_cost = int(offer_json['fullCost']),
                        qntunits =offer_json['qntunits'] ,
                        quantity = offer_json['quantity'] ,
                        validity = parser.parse(offer_json['validity']) ,
                        trade_category = offer_json['attrTradings']['name']
                    )
                    offer.save()
                except IntegrityError as e:
                    Offer.objects.filter(number=offer_json['id']).update(
                        number = offer_json['id'],
                        product_name = offer_json['productname'],
                        country = offer_json['country'],
                        price = float(offer_json['price']) ,
                        currency = offer_json['currency'] ,
                        full_cost = int(offer_json['fullCost']),
                        qntunits =offer_json['qntunits'] ,
                        quantity = offer_json['quantity'] ,
                        validity = parser.parse(offer_json['validity']) ,
                        trade_category = offer_json['attrTradings']['name']
                    )
            if len(response.json()['list'])< 2:
                print(i,'thats all')
        except Exception as e:
            raise e



def get_offers_for_bid(bid_id:int, token:str, pages:int) -> None:
    cookies = {
    'session-cookie': '1730597102a006174148f3bcbeb261f5bb9fda7a3b13720d446e24a3eb4d82c71ec6c71f3733a3f12a36a7d6952eca14',
}

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'session-cookie=1730597102a006174148f3bcbeb261f5bb9fda7a3b13720d446e24a3eb4d82c71ec6c71f3733a3f12a36a7d6952eca14',
        'Origin': 'https://ppt.butb.by',
        'Referer': 'https://ppt.butb.by/ppt-new/catalog-demands',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-auth-token': '{'+f'{token}'+'}',
        'x-language': 'ru',
    }
    for i in range(pages):
        json_data = {
            'status': 2,
            'counterDemand': bid_id,
            'paginationFilters': {
                'page': 0,
                'pageSize': 50,
            },
            'searchFilters': {},
        }
        response = requests.post('https://ppt.butb.by/PPT-Rest/api/offers/own', cookies=cookies, headers=headers, json=json_data)
        for j in range(len(response.json()['list'])):
            offer_json = response.json()['list'][j]
            Offer.objects.filter(number=offer_json['id']).update(
                bid_id = int(bid_id)
            )
            if (len(response.json()['list']) < 2):
                print(i, 'thats all')


def submit_offer(bid_id, offer_id, user_id, token):
    headers = {
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'x-language': 'ru',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://ppt.butb.by/ppt-new/catalog-demands',
    'x-auth-token': '{'+f'{token}'+'}',
    'sec-ch-ua-platform': '"Windows"',
}

    json_data = {
        'idOffer': offer_id,
    }
    try:
        # response = requests.post(f'https://ppt.butb.by/PPT-Rest/api/counteroffers/{bid_id}', headers=headers, json=json_data)
        bid = Bid.objects.get(purchase_order=int(bid_id))
        offer = Offer.objects.get(number=offer_id)
        bid.offer.add(offer)
        Bid.objects.filter(purchase_order=int(bid_id)).update(trader=user_id)
        Offer.objects.filter(number=int(offer_id)).update(trader=user_id)
        return 200
    except Exception as e:
        raise e

if __name__ == '__main__':
    get_offers_for_bid(539014,'37BF5AA0-D976-4BAE-9B9E-67730920C5D9', 10)

    parse_offers('905DD217-E592-4609-A9F0-6343EF70FD02',20)

    parse_status_of_trades('C99967A4-1A46-400F-A086-53FAE7E46D43',10)