from bs4 import BeautifulSoup
from typing import Iterable


def is_name_in_list(name: str, data: list) -> bool or list:
    for i, j in enumerate(data):
        if name in j.keys():
            return [True, i]
    return False


def parse_preview_data(data_html: str) -> Iterable[dict]:
    soup = BeautifulSoup(data_html, 'lxml')
    product_divs = soup.find_all('div', {'class': 'block___ProductList___1lpGO'})

    data = {
        'name': None,
        'color': None,
        'price': None,
        'status': None,
        # 'sizes': [{'size': 'size', 'status': 'enable/disable'}] if product isn't sold out
    }
    products = []

    for i in product_divs:
        product_data = data.copy()
        name = i.find('p', {'class': 'title___Description___2qBc1 text___Text___2X-M-'})
        product_data['name'] = name.text
        color = i.find('em', {'class': 'em___Description___tJzVm'})
        product_data['color'] = color.text
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
        products.append(product_data)
    for i in products:
        yield i