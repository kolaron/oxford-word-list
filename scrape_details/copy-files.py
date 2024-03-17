import os
import shutil

from database.entity import Definition, Word
from scrape_details.scrape import get_word_from_url

source_dir = '/home/kolar/Projects/oxford-word-list/html_downloader/html_files'
target_dir = '/home/kolar/Projects/oxford-word-list/html_downloader/html_files_error/'

def is_file_exists(file, words):
    exists = False
    for word in words:
        if file.endswith(get_word_from_url(word.get().definition_url)+'.htm'):
            exists = True
            break
    return exists

if __name__ == "__main__":
  words = Word.select().where(Word.id.not_in(Definition.select(Definition.word_id)))
  print(words.count())
  for word in words:
    filename = get_word_from_url(word.definition_url)+'.htm'
    src_file = os.path.join(source_dir, filename)
    if not os.path.exists(src_file):
      # shutil.copy(src_file, target_dir)  # copies src_file to target_dir
      print(f'MISSING: {filename}')