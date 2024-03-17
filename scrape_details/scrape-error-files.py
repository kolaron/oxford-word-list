from bs4 import Tag

from database.entity import Definition, SentenceDefinition, Word
from scrape_details.scrape import scrape_oxford


def find_definitions(soup, wordEntity: Word) -> list[Tag]:
    senses = soup.find("ol", class_="senses_multiple")
    senses = soup.find("ol", class_="sense_single") if senses is None else senses
    if senses is None:
        print(f"CHYBA definitions was not found: {wordEntity.id}")
    return senses.find_all("li", class_="sense") if senses else []


def find_definition(sense):
    return sense.find("span", {"class": "def"})


def find_examples(sense):
    examples_div = sense.find("ul", class_="examples")
    if examples_div is None:
        return []
    return [ex.text.strip() for ex in examples_div.find_all("span", class_="x")]


def scrape(wordEntity, soup, filepath):
    # For each sense, find the definition and example sentences
    for definition_block in find_definitions(soup, wordEntity):
        definition = find_definition(definition_block)
        if definition is None:
            print(
                f"CHYBA sence: {definition}, filePath: {filepath}, url: {wordEntity.definition_url}"
            )
            continue
        definition_entity, created = Definition.get_or_create(
            word_id=wordEntity.id,
            defaults={"definition": definition.text, "word_id": wordEntity.id},
        )
        if definition_entity is None:
            continue
        examples = find_examples(definition_block)
        list = []
        for example in examples:
            example_entity, exampleCreated = SentenceDefinition.get_or_create(
                definition_id=definition_entity.id,
                defaults={"sentence": example, "definition_id": definition_entity.id},
            )
            list.append(example)
        print(f"Examples: {list}")


if __name__ == "__main__":
    scrape_oxford(scrape)
