import requests
from typing import Optional, Iterable
import tipo_parser
import urllib.parse


SEARCH_STRING = 'бухгалтер'
LAST_PAGE = None


def domain() -> str:
    return 'www.work.ua'


def get_search_url(job_type: str = None, page: int = None) -> Optional[str]:
    if job_type is None:
        return
    if page is None:
        return f'https://{domain()}/jobs-kyiv-{job_type}/'
    return f'https://{domain()}/jobs-kyiv-{job_type}/?page={page}'


def send_request(url: str) -> str:
    resp = requests.get(url)
    final_data = resp.text
    return final_data


def save_html(html: str):
    with open('page.html', 'w') as file:
        file.write(html)


def get_full_url(url_tail: str) -> str:
    """Make full url from tail and domain"""
    return f'https://{domain()}{url_tail}'


def get_phone_url(url_tail: str) -> str:
    return f'https://{domain()}{url_tail}/ajax/get-jobs-data/'


def send_request_for_vacansy(url_tail: str) -> str:
    url = get_full_url(url_tail)
    resp = requests.get(url)
    final_data = resp.text
    return final_data


def parse_one_page_all_data(page_number=1) -> Iterable[dict]:
    global LAST_PAGE
    url = get_search_url(SEARCH_STRING, page=page_number)
    response_text = send_request(url)
    if LAST_PAGE is None:
        LAST_PAGE = tipo_parser.parse_last_page(response_text)

    all_data = {
        'preview_data': None,
        'full_data': None,
        #'phone-number': None,
    }

    data = tipo_parser.parse_preview_data(response_text, page_number)
    for element in data:
        full_vacancy_raw_data = send_request_for_vacansy(element['url_tail'])
        answer = all_data.copy()
        answer['preview_data'] = element
        answer['full_data'] = tipo_parser.parse_full_vacancy(full_vacancy_raw_data)
        if tipo_parser.is_phone_number_on_page(full_vacancy_raw_data):
            phone_number_raw_data = send_request_phone_number(element['url_tail'])
            answer['phone-number'] = tipo_parser.parse_phone_number(phone_number_raw_data)
        yield answer


def pagination() -> Iterable[dict]:
    global LAST_PAGE
    for element in parse_one_page_all_data():
        yield element

    for page_number in range(2, LAST_PAGE+1):
        print(page_number)
        for element in parse_one_page_all_data(page_number):
            yield element


def send_request_phone_number(url_tail) -> Optional[str]:
    url = get_phone_url(url_tail)
    resp = requests.post(url)
    if resp.status_code == 200:
        return urllib.parse.unquote_plus(resp.text)
    return


if __name__ == '__main__':
    lol = pagination()
    for i in lol:
        print(i)
