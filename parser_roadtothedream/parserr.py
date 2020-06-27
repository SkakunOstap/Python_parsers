from bs4 import BeautifulSoup
from typing import Iterable


def domain() -> str:
    """Return domain of site"""
    return "roadtothedream.com"


def parse_product_description(data_html: str) -> str:
    soup = BeautifulSoup(data_html, 'lxml')
    description_div = soup.find('div', {'class': 'information__block__description___Information___KWE9m'})
    description = description_div.find('p').text
    return description


def parse_preview_data(data_html: str) -> Iterable[dict]:
    soup = BeautifulSoup(data_html, 'lxml')
    product_divs = soup.find_all('div', {'class': 'block___ProductList___1lpGO'})

    data = {
        'name': None,
        'color': None,
        'url': None,
        'description': None,
        'price': None,
        'status': None,
        # 'sizes': [{'size': 'size', 'status': 'enable/disable'}] if product isn't sold out
    }

    for i in product_divs:
        product_data = data.copy()
        name = i.find('p', {'class': 'title___Description___2qBc1 text___Text___2X-M-'})
        product_data['name'] = name.text
        color = i.find('em', {'class': 'em___Description___tJzVm'})
        product_data['color'] = color.text
        url_tail = i.find('a').get('href')
        product_data['url'] = "https://" + domain() + url_tail
        price = i.find('div', {'class': 'price___Price___2jC3y'})
        product_data['price'] = price.text
        status = i.find('div', {'class': 'resaled___Sizes___kiNpI'})
        if status is None:
            product_data['status'] = 'В наличии'
            size_divs = i.find_all('div', {'class': 'btn___SizeBtn___A4DSs'})
            sizes = []
            for j in size_divs:
                size = j.text
                if j.get('class') == ['btn___SizeBtn___A4DSs']:
                    size_status = 'присутствует'
                else:
                    size_status = 'отсуствует'
                sizes.append({'size': size, 'status': size_status})
            product_data['sizes'] = sizes
        else:
            product_data['status'] = 'Распродано'
        yield product_data
