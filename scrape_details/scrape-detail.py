from bs4 import Tag

from database.entity import Definition, SentenceDefinition, get_database
from scrape_details.scrape import scrape_oxford


def find_definitions(soup) -> list[Tag]:
    senses_multiple = soup.find('ol', class_='senses_multiple')
    print(senses_multiple)
    return senses_multiple.find_all('li', class_='sense') if senses_multiple else []

def find_definition(sense):
    return sense.find('span', {'class': 'def'})

def find_examples(sense):
    examples_div = sense.find('ul', class_='examples')
    if examples_div is None:
        return []
    return [ex.text.strip() for ex in examples_div.find_all('span', class_='x')]

def scrape(wordEntity, soup, filepath, url):
  # For each sense, find the definition and example sentences
  for definition_block in find_definitions(soup):
    definition = find_definition(definition_block)
    if definition is None:
      print(f'CHYBA sence: {definition}, filePath: {filepath}, url: {url}')
      continue
    def_text = definition.text
    definition_entity, created = Definition.get_or_create(definition=def_text, defaults={'definition': def_text, 'word_id': wordEntity.id})
    if definition_entity is None:
      continue
    print(f'Definition: {definition_entity}')
    examples = find_examples(definition_block)
    # list = []
    for example in examples:
        example_entity, exampleCreated = SentenceDefinition.get_or_create(sentence=example, defaults={'sentence': example, 'definition_id': definition_entity.id})
    # list.append({'example': example})
    # print(f'Examples: {list}')
    # rename_file(url, filepath, subdir)
    # return

if __name__ == "__main__":
  scrape_oxford(scrape)