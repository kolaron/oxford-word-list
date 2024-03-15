import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from converters import oxford
from database.entity import Word


def parse(item: BeautifulSoup) -> oxford.Entry:
    word = item.get("data-hw")
    level = item.get("data-ox5000")

    pos_el = item.find("span", class_="pos")
    pos = pos_el.string if pos_el else None

    definition_el = item.find("a")
    definition_url = definition_el.get("href") if definition_el else None
    if definition_url is None:
        definition_url = None
    else:
        parsed_url = urlparse(definition_url)
        definition_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path


    voice_el = item.find("div", class_="pron-us")
    voice_url = voice_el.get("data-src-ogg") if voice_el else None
    voice_url = oxford.BASE_URL + voice_url if voice_url else None
    
    # hidden = item.get("class") == ["hidden"]
    # if hidden:
    #     return None

    return oxford.Entry(word, level, pos, definition_url, voice_url)


if __name__ == "__main__":
    oxford.to_csv(sys.argv[1], parse)
