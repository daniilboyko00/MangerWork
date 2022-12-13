import requests
import os
import django
from django.db.utils import IntegrityError
import sys
sys.path.append(r"D:\MangerWork\app")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from api.models import Offer
from dateutil import parser



def parse_trades():
    cookies = {
        '_ym_uid': '1669898926163754051',
        '_ym_d': '1669898926',
        '_gcl_au': '1.1.72392559.1669966434',
        '_gid': 'GA1.2.33312829.1670247244',
        '_ym_isad': '1',
        'session-cookie': '172e3b0c542bd5f04148f3bcbeb261f58a4794d09efe4f6200e557f20fe495793b4d72675710957debaa3129311971b1',
        '_ym_visorc': 'w',
        '_ga': 'GA1.1.338988082.1669966434',
        '_ga_JBLWJN4EG6': 'GS1.1.1670346679.5.1.1670346808.21.0.0',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': '_ym_uid=1669898926163754051; _ym_d=1669898926; _gcl_au=1.1.72392559.1669966434; _gid=GA1.2.33312829.1670247244; _ym_isad=1; session-cookie=172e3b0c542bd5f04148f3bcbeb261f58a4794d09efe4f6200e557f20fe495793b4d72675710957debaa3129311971b1; _ym_visorc=w; _ga=GA1.1.338988082.1669966434; _ga_JBLWJN4EG6=GS1.1.1670346679.5.1.1670346808.21.0.0',
        'Origin': 'https://ppt.butb.by',
        'Referer': 'https://ppt.butb.by/ppt-new/profile/bids/downwardExpirationDate',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-auth-token': '{646CCCA0-352A-42B8-A26D-6C83B19DD569}',
        'x-language': 'ru',
    }

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
        'paginationFilters': {},
    }

    response = requests.post('https://ppt.butb.by/PPT-Rest/api/trades',   headers=headers, json=json_data)
    print(response.json())

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
                    offer.save()
                except IntegrityError:
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
        except TypeError:
            raise TypeError

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

# get_offers_for_bid(539014,'905DD217-E592-4609-A9F0-6343EF70FD02', 10)

# parse_offers('905DD217-E592-4609-A9F0-6343EF70FD02',20)