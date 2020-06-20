from bs4 import BeautifulSoup
from typing import Iterable


def are_games_on_page(data_html: str) -> bool:
    if 'По вашему запросу ничего не найдено. Повторите попытку изменив запрос' in data_html:
        return False
    return True


def parse_games(data_html: str) -> Iterable[dict] or None:
    if are_games_on_page(data_html):
        soup = BeautifulSoup(data_html, 'lxml')
        items = soup.find_all('li', {'class': 'catalog-item js-list-item'})

        dict_example = {
            'name': None,
            'rating': None,
            'type': None,
            'date': None,
            'info': None,
        }

        for element in items:
            dict_copy = dict_example.copy()
            dict_copy['name'] = element.find('a', {'class': 'color-ios'}).text.strip()
            dict_copy['rating'] = element.find('div', {'class': 'catalog-item__rating'}).find('div').text.strip()
            dict_copy['type'] = element.find('a', {'class': 'button button_gray_bordered catalog-item__genre-button'}).text.strip()
            dict_copy['date'] = element.find('time', {'class': 'catalog-item__date'}).text.strip()
            dict_copy['info'] = element.find('p', {'class': 'catalog-item__description'}).text.strip()
            yield dict_copy
    return