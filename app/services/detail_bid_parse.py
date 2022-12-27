import requests
import json
import sys
sys.path.append(r"D:\MangerWork\app")

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from api.models import Bid



def save_and_return_detail_bid_json(id:int):
    cookies = {
        '_ym_uid': '1669898926163754051',
        '_ym_d': '1669898926',
        '_gcl_au': '1.1.72392559.1669966434',
        'session-cookie': '172ee82ea7dcef5a4148f3bcbeb261f52ce24c47456e1174df2c59791f19934ccc88e01a6f47bebd70ed08703529ce78',
        '_gid': 'GA1.2.245389114.1670588999',
        '_dc_gtm_UA-86108420-3': '1',
        '_ga': 'GA1.1.338988082.1669966434',
        '_ym_isad': '1',
        '_ym_visorc': 'w',
        '_ga_JBLWJN4EG6': 'GS1.1.1670588998.6.0.1670589008.50.0.0',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': '_ym_uid=1669898926163754051; _ym_d=1669898926; _gcl_au=1.1.72392559.1669966434; session-cookie=172ee82ea7dcef5a4148f3bcbeb261f52ce24c47456e1174df2c59791f19934ccc88e01a6f47bebd70ed08703529ce78; _gid=GA1.2.245389114.1670588999; _dc_gtm_UA-86108420-3=1; _ga=GA1.1.338988082.1669966434; _ym_isad=1; _ym_visorc=w; _ga_JBLWJN4EG6=GS1.1.1670588998.6.0.1670589008.50.0.0',
        'Referer': 'https://ppt.butb.by/ppt-new/catalog-demands/order/538406',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-language': 'ru',
    }

    response = requests.get(f'https://ppt.butb.by/PPT-Rest/api/demands/{id}', cookies=cookies, headers=headers)
    resp_json = response.json()

    bid_data = {
        'id': resp_json['id'],
        'brandname': resp_json['product']['brandname'],
        'producing_country': resp_json['product']['country'],
        'product_information': resp_json['product']['description'],
        'terms_of_payment':resp_json['termsOfSale']['deliverytime']['description'],
        'delivery_conditions':resp_json['termsOfSale']['deliverycond']['description'],
    }
    Bid.objects.filter(id=id).\
        update(brand=bid_data['brandname'],
        producing_country=bid_data['producing_country'],
        product_information=bid_data['product_information'],
        terms_of_payment=bid_data['terms_of_payment'],
        delivery_conditions=bid_data['delivery_conditions'] )

    return json.dumps(bid_data, ensure_ascii=False)

# r = save_and_return_detail_bid_json(538375)
# print(r)