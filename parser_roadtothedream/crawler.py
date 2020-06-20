import requests
from typing import Optional
import parserr


def domain() -> str:
    """Return domain of site"""
    return "roadtothedream.com/mens"


def send_request(url: str) -> str:
    resp = requests.get(url)
    final_data = resp.text
    return final_data


if __name__ == '__main__':
    data = parserr.parse_preview_data(send_request('https://' + domain()))
    for i in data:
        print(i)