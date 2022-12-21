import requests
import time
import sys

sys.path.append(r"D:\MangerWork\app")

import os
import django
from django.db.utils import IntegrityError
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from api.models import Bid
from dateutil import parser
from datetime import datetime


def parse_bid(num_of_pages: int):
    cookies = {
        '_gcl_au': '1.1.1396394166.1669884021',
        '_ym_uid': '1669884023824212853',
        '_ym_d': '1669884023',
        'session-cookie': '172de97d08328bc64148f3bcbeb261f53ce6d0afd8aabb40f3ea265e09ac67e18054310bc70e4149ede125079cefc8be',
        '_gid': 'GA1.2.1850910485.1670248293',
        '_ga': 'GA1.1.1784619702.1669884022',
        '_ga_JBLWJN4EG6': 'GS1.1.1670254636.4.0.1670254636.60.0.0',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': '_gcl_au=1.1.1396394166.1669884021; _ym_uid=1669884023824212853; _ym_d=1669884023; session-cookie=172de97d08328bc64148f3bcbeb261f53ce6d0afd8aabb40f3ea265e09ac67e18054310bc70e4149ede125079cefc8be; _gid=GA1.2.1850910485.1670248293; _ga=GA1.1.1784619702.1669884022; _ga_JBLWJN4EG6=GS1.1.1670254636.4.0.1670254636.60.0.0',
        'Origin': 'https://ppt.butb.by',
        'Referer': 'https://ppt.butb.by/ppt-new/catalog-demands',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-language': 'ru',
    }
    for i in range(num_of_pages):
        json_data = {
            'gpcCode': '',
            'mainFilters': {
                'typeTrade': {
                    'decrease_date': False,
                    'decrease_term': False,
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
        response = requests.post('https://ppt.butb.by/PPT-Rest/api/demands/gpc', cookies=cookies, headers=headers, json=json_data)
        for j in range(len(response.json()['list'])):
            bid_json = response.json()['list'][j]
            try:
                if str(bid_json['statusOffer']['code']) == '5':
                    Bid.objects.filter(purchase_order = int(bid_json['id'])).delete()
                    continue
            except:
                pass
            try:
                bid = Bid(
                    purchase_order = int(bid_json['id']),
                    application_date =  parser.parse(bid_json['activity']),
                    application_validity_period = parser.parse(bid_json['validity']),
                    procurement_name = bid_json['productname'],
                    product_information = None,
                    brand = None,
                    buyer_country = bid_json['country'],
                    qntunits = bid_json['qntunits'],
                    producing_country = None,
                    terms_of_payment = None,
                    delivery_conditions = None,
                    delivery_time = None,
                    exposure_time =  parser.parse(bid_json['exposure']),
                    application_is_bidding = bid_json['attrTradings']['name'],
                    price = bid_json['price'],
                    number_of_goods = bid_json['quantity'],
                    cost = bid_json['fullCost'],
                    currency = bid_json['currency'],
                    technical_documentation_file_name = None,
                    application_link = f"https://ppt.butb.by/ppt-new/catalog-demands/order/{bid_json['id']}",
                    scraping_date = datetime.now(tz=timezone.utc),
                    slug = int(bid_json['id']),
                    tnvedcode = int(bid_json['tnvedcode']),
                    number_of_subcount = bid_json.get('viewSubcount') if bid_json.get('viewSubcount') else None,
                    subcount_link = f"https://ppt.butb.by/ppt-new/import-substitution/offers?tnvedCode={bid_json['tnvedcode']}"
                    )
                bid.save()
            except IntegrityError:
                Bid.objects.filter(purchase_order=bid_json['id']).update(
                    purchase_order = int(bid_json['id']),
                    application_date =  parser.parse(bid_json['activity']),
                    application_validity_period = parser.parse(bid_json['validity']),
                    procurement_name = bid_json['productname'],
                    product_information = None,
                    brand = None,
                    buyer_country = bid_json['country'],
                    qntunits = bid_json['qntunits'],
                    producing_country = None,
                    terms_of_payment = None,
                    delivery_conditions = None,
                    delivery_time = None,
                    exposure_time =  parser.parse(bid_json['exposure']),
                    application_is_bidding = bid_json['attrTradings']['name'],
                    price = bid_json['price'],
                    number_of_goods = bid_json['quantity'],
                    cost = bid_json['fullCost'],
                    currency = bid_json['currency'],
                    technical_documentation_file_name = None,
                    application_link = f"https://ppt.butb.by/ppt-new/catalog-demands/order/{bid_json['id']}",
                    slug = int(bid_json['id']),
                    tnvedcode = int(bid_json['tnvedcode']),
                    number_of_subcount = bid_json.get('viewSubcount') if bid_json.get('viewSubcount') else None,
                    subcount_link = f"https://ppt.butb.by/ppt-new/import-substitution/offers?tnvedCode={bid_json['tnvedcode']}",
                    scraping_date = datetime.now(tz=timezone.utc)
                )
            if len(response.json()['list']) < 80:
                print(i, 'thats all')
                break

if __name__ == '__main__':
    r = parse_bid(100)
