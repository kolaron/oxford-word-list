import os
from typing import Callable
from bs4 import BeautifulSoup, ResultSet, Tag
from database.entity import Definition, SentenceDefinition, Word, get_database

HTML_FOLDER = '/home/kolar/Projects/oxford-word-list/html_downloader/html_files'

def get_image(sense):
    android_app_tags = sense.find_all('a', {'class': 'android-app'})

    # find all 'img' tags inside 'a' tags with class 'android-app'
    android_app_imgs = [img for tag in android_app_tags for img in tag.find_all('img')]
    
    img_tag = sense.find('img')
    if img_tag is not None and img_tag not in android_app_imgs:
        return img_tag['src']

def rename_file(url, oldpath, subdir):
    new_name = get_word_from_url(url)
    if new_name is None:
        return
    new_name = new_name+'.htm' if not new_name.endswith('.htm') else new_name
    if new_name == oldpath.split('\\')[-1]:
        return
    new_file = os.path.join(subdir, new_name)
    try:
        os.rename(oldpath, new_file)
    except FileExistsError:
        print(f'CHYBA: soubor jiz existuje: {new_file}')

'''
Scrape local html files. And get the word, definition, and example sentences.
'''
def scrape_oxford(parse_fn: Callable[[Word,BeautifulSoup, str, str], None]):
    for subdir, dirs, files in os.walk(HTML_FOLDER):
        for file in files:
            # Get the full file path by joining the directory path and file name
            filepath = os.path.join(subdir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Find the word
            find_word = soup.find('h1', class_='headword')
            if find_word is None:
                print(f'CHYBA find_word: {find_word}, filePath: {filepath}')
                continue
            link = soup.find('link', rel='canonical')
            url = link['href']
            try:
                wordEntity = Word.get(Word.definition_url == url)
            except Word.DoesNotExist:
                # print(f'CHYBA DB nenalezeno word: {word}, filePath: {filepath}, url: {url}')
                continue
            with get_database().atomic():
                parse_fn(wordEntity, soup, filepath, url[0])

# if __name__ == "__main__":
#     scrape_oxford()
