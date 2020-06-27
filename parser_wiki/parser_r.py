from bs4 import BeautifulSoup


def parse_preview_data(data_html: str) -> str:
    soup = BeautifulSoup(data_html, 'lxml')
    content_div = soup.find('div', {'class': 'mw-parser-output'})
    return content_div.text