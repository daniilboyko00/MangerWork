import requests

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
    'x-auth-token': '{B2B5A637-B1BE-4627-91B2-B11771F36D1F}',
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
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"typeTrade":4,"mainFilters":{"roleInTrade":3,"tradeStatusCode":null},"searchFilters":{"searchString":null,"productName":null,"fabricator":null,"regNum":null,"description":null,"tnvedCode":null},"paginationFilters":{}}'
#response = requests.post('https://ppt.butb.by/PPT-Rest/api/trades', cookies=cookies, headers=headers, data=data)