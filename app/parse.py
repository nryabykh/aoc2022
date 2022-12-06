"""
Parses data from https://adventofcode.com/
"""

from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import time
from app.secrets import get_session_id

PARSE_EMPTY = 'Not Available'


@dataclass
class DayInfo:
    day: int
    url: str
    title: str
    texts: list[tuple[str, str]]


def get_day_info(last_day: int) -> list[DayInfo]:
    cookies = {'session': get_session_id()}
    base_url = 'https://adventofcode.com/2022/day'
    days_data = []
    stop = False
    for day in range(1, last_day+1):
        url = f'{base_url}/{day}'
        if stop:
            days_data.append(DayInfo(day, url, PARSE_EMPTY, []))
            continue

        html = requests.get(url, cookies=cookies)
        if html.status_code != 200:
            days_data.append(DayInfo(day, url, PARSE_EMPTY, []))
            stop = True
            continue

        soup = BeautifulSoup(html.content, 'html.parser')
        title = soup.find_all('h2')[0].get_text()
        texts = list(map(lambda x: (x.name, x.text), soup.find_all(['p', 'pre'])))
        days_data.append(DayInfo(day, url, title, texts))
        time.sleep(0.5)

    return days_data
