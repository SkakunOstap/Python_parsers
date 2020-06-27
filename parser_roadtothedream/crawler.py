import requests
from typing import Optional
import parserr


def domain() -> str:
    """Return domain of site"""
    return "roadtothedream.com"


def send_request(url: str) -> str:
    resp = requests.get(url)
    final_data = resp.text
    return final_data


if __name__ == '__main__':
    data = parserr.parse_preview_data(send_request('https://' + domain() + "/mens"))
    for i in data:
        j = i.copy()
        j['description'] = parserr.parse_product_description(send_request(j['url']))
        print(j)
        break