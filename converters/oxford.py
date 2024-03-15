"""
Parse Oxford word lists from html to csv.
https://www.oxfordlearnersdictionaries.com/wordlists/

First save the list as html (only the li's inside the list ul).
Then run the tool:

    python3 -m converters.oxford-5k data/oxford-5k.html data/oxford-5k.csv
    python3 -m converters.oxford-opal data/oxford-opal.html data/oxford-opal.csv
    python3 -m converters.oxford-phrase data/oxford-phrase.html data/oxford-phrase.csv

After that, data/*.csv will contain lists in csv.
"""

import csv
import dataclasses
from typing import Iterator, Callable
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Tag
from database.cefr_service import CerfService

from database.entity import Word
BASE_URL = "https://www.oxfordlearnersdictionaries.com"


@dataclasses.dataclass
class Entry:
    word: str
    level: str
    pos: str
    definition_url: str
    voice_url: str = None

def load_source(filename: str) -> BeautifulSoup:
    text = ""
    with open(filename) as file:
        text = file.read()
    return BeautifulSoup(text, "lxml")


def reader(soup: BeautifulSoup, parse_fn: Callable[[BeautifulSoup], Entry]) -> Iterator[Entry]:
    for item in soup.body:
        if not isinstance(item, Tag):
            continue
        entry = parse_fn(item)
        if entry is None:
            continue
        yield entry


def writer(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        header = [field.name for field in dataclasses.fields(Entry)]
        writer.writerow(header)
        while True:
            row = yield
            writer.writerow(row)

def to_csv(in_filename: str, parse_fn: Callable[[BeautifulSoup], Entry]):
    soup = load_source(in_filename)
    count = 0
    for entry in reader(soup, parse_fn):
        count += 1
        try:
            Word.get(Word.definition_url == entry.definition_url)
        except Word.DoesNotExist:
            print({'WORD': entry.word, 'TYPE_ID': 2,'LEVEL_ID': CerfService.get_id_by_string(entry.level), 'POS': entry.pos, 'DEFINITION_URL': entry.definition_url, 'VOICE_URL': entry.voice_url, 'DEFINITION_ID': None})
        # Word.get_or_create(definition_url=entry.definition_url, defaults={'WORD': entry.word, 'TYPE_ID': 2,'LEVEL_ID': CerfService.get_id_by_string(entry.level), 'POS': entry.pos, 'DEFINITION_URL': entry.definition_url, 'VOICE_URL': entry.voice_url, 'DEFINITION_ID': None})
    # print(count)
    