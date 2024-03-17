import os
import shutil
from config import get_html_files_path

from database.entity import Definition, Word

target_dir = "C:\\Users\\Kolar\\IdeaProjects\\oxford-word-list\\html_downloader\\html_files_error\\"

def is_file_exists(file, words):
    exists = False
    for word in words:
        if file.endswith(word.get_word_from_url() + ".htm"):
            exists = True
            break
    return exists

if __name__ == "__main__":
    words = Word.select().where(Word.id.not_in(Definition.select(Definition.word_id)))
    print(words.count())
    for word in words:
        filename = word.get_word_from_url() + ".htm"
        src_file = os.path.join(get_html_files_path(), filename)
        if not os.path.exists(src_file):
            print(f"MISSING: {filename}")
            continue
        # shutil.copy(src_file, target_dir)  # copies src_file to target_dir
