import requests
import parser_r


def domain():
    return "https://ru.wikipedia.org/wiki/"


def send_request(url: str) -> str:
    resp = requests.get(url)
    final_data = resp.text
    return final_data


name = input()
print(parser_r.parse_preview_data(send_request(domain() + name)))