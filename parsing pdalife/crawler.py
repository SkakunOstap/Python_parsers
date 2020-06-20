import requests
import parserr


def domain() -> str:
    return "https://pdalife.ru/ios/igry/sort-by/new/"


def send_request(url: str, page: int = 1) -> str:
    if page > 1:
        resp = requests.get(f"{url}page-{page}/")
    else:
        resp = requests.get(url)
    return resp.text


def find_all_games(last_page: int = 1) -> dict:
    games = []
    for i in range(last_page):
        data_html = send_request(domain(), i+1)
        page_games = parserr.parse_games(data_html)
        if page_games is None:
            print(f"Page {i+1} does not exist")
            break
        for i in page_games:
            games.append(i)
    for i in games:
        yield i


games = find_all_games(2)
for i in games:
    print(i)