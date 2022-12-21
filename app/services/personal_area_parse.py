import requests
import os
import django
from django.db.utils import IntegrityError
from django.utils import timezone
import sys
sys.path.append(r"D:\MangerWork\app")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from api.models import Offer, Bid, Notification
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
                print(2)
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
        'session-cookie': '1730f7b9122a04d14148f3bcbeb261f5312b4a84cf06994c152e295b13f7925d5986b1ed8220d9f596429b09510f1b90',
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
                    print(e)
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
                break
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
        Bid.objects.filter(purchase_order=int(bid_id)).update(trader=user_id, activityStatus=1)
        return 200
    except Exception as e:
        raise e


def parse_notification(token):
    cookies = {
        '_gcl_au': '1.1.996378576.1671528647',
        '_gid': 'GA1.2.1922921561.1671528647',
        '_ym_uid': '1671528647293545921',
        '_ym_d': '1671528647',
        '_ga': 'GA1.1.1588590972.1671528647',
        'session-cookie': '173276804bb64ce04148f3bcbeb261f56dd0969f7c1f6b4cc80c1c7ec78b18bde38c09fc2a4ac127888f9d8caac21f34',
        '_ga_JBLWJN4EG6': 'GS1.1.1671534419.2.1.1671534420.59.0.0',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': '_gcl_au=1.1.996378576.1671528647; _gid=GA1.2.1922921561.1671528647; _ym_uid=1671528647293545921; _ym_d=1671528647; _ga=GA1.1.1588590972.1671528647; session-cookie=173276804bb64ce04148f3bcbeb261f56dd0969f7c1f6b4cc80c1c7ec78b18bde38c09fc2a4ac127888f9d8caac21f34; _ga_JBLWJN4EG6=GS1.1.1671534419.2.1.1671534420.59.0.0',
        'Referer': 'https://ppt.butb.by/ppt-new/profile/my-profile',
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

    response = requests.get('https://ppt.butb.by/PPT-Rest/api/notify/all', cookies=cookies, headers=headers)
    print(response.json()['list'])
    for notify in response.json()['list']:
        try:
            notification = Notification(
                id = notify['idNotify'],
                date = parser.parse(notify['dateReg']),
                message = notify['message']
            )
            notification.save()
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    parse_status_of_trades('75D3B99E-9E5C-46D1-B5BA-6B9C9FECADB6', 20)
    # parse_notification('75D3B99E-9E5C-46D1-B5BA-6B9C9FECADB6')
