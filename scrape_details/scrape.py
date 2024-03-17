import os
from typing import Callable
from bs4 import BeautifulSoup
from config import get_html_files_path
from database.entity import Word, get_database


def get_image(sense):
    android_app_tags = sense.find_all("a", {"class": "android-app"})

    # find all 'img' tags inside 'a' tags with class 'android-app'
    android_app_imgs = [img for tag in android_app_tags for img in tag.find_all("img")]

    img_tag = sense.find("img")
    if img_tag is not None and img_tag not in android_app_imgs:
        return img_tag["src"]


def rename_file(word: Word, oldpath, subdir):
    new_name = word.get_word_from_url()
    if new_name is None:
        return
    new_name = new_name + ".htm" if not new_name.endswith(".htm") else new_name
    if new_name == oldpath.split("\\")[-1]:
        return
    new_file = os.path.join(subdir, new_name)
    try:
        os.rename(oldpath, new_file)
    except FileExistsError:
        print(f"CHYBA: soubor jiz existuje: {new_file}")


"""
Scrape local html files. And get the word, definition, and example sentences.
"""


def scrape_oxford(parse_fn: Callable[[Word, BeautifulSoup, str], None]):
    for subdir, dirs, files in os.walk(get_html_files_path()):
        for file in files:
            # Get the full file path by joining the directory path and file name
            filepath = os.path.join(subdir, file)
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                url = soup.find("link", rel="canonical")["href"]
                try:
                    wordEntity = Word.get(Word.definition_url == url)
                except Word.DoesNotExist:
                    print(
                        f"CHYBA DB nenalezeno word: {wordEntity}, filePath: {filepath}, url: {url}"
                    )
                    continue
                with get_database().atomic():
                    parse_fn(wordEntity, soup, filepath)
