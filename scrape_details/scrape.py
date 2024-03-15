import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from database.entity import Definition, SentenceDefinition, Word, get_database

HTML_FOLDER = 'C:\\Users\\Kolar\\IdeaProjects\\oxford-word-list\\html_downloader\\html_files'
# HTML_FOLDER = 'C:\\Users\\Kolar\\IdeaProjects\\oxford-word-list\\html_downloader\\error_files'
# HTML_FOLDER = 'C:\\Users\\Kolar\\IdeaProjects\\oxford-word-list\\html_downloader\\test'

def get_word_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    parts = path.split('/')
    return parts[-1]

def find_definitions(soup):
    senses_multiple = soup.find('ol', class_='senses_multiple')
    return senses_multiple.find_all('li', class_='sense') if senses_multiple else []

def find_definition(sense):
    return sense.find('span', {'class': 'def'})

def find_examples(sense):
    examples_div = sense.find('ul', class_='examples')
    if examples_div is None:
        return []
    return [ex.text.strip() for ex in examples_div.find_all('span', class_='x')]

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
def scrape_oxford():
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
            senses = find_definitions(soup)
            # For each sense, find the definition and example sentences
            with get_database().atomic():
                for sense in senses:
                    img_url = get_image(sense)
                    sence = find_definition(sense)
                    if sence is None:
                        print(f'CHYBA sence: {sence}, filePath: {filepath}, url: {url}')
                        continue
                    def_text = sence.text
                    definition_entity, created = Definition.get_or_create(definition=def_text, defaults={'definition': def_text, 'word_id': wordEntity.id})
                    if definition_entity is None:
                        continue
                    if img_url is None or img_url == definition_entity.img_url:
                        continue
                    definition_entity.img_url = img_url
                    definition_entity.save()
                    # print(f'Definition: {definition}')
                    # examples = find_examples(sense)
                    # list = []
                    # for example in examples:
                    #     example_entity, exampleCreated = SentenceDefinition.get_or_create(sentence=example, defaults={'sentence': example, 'definition_id': definition_entity.id})
                    #     list.append({'example': example})
                    # print(f'Examples: {list}')
            rename_file(url, filepath, subdir)
            # return

if __name__ == "__main__":
    scrape_oxford()
