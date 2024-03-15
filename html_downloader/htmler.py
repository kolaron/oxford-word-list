import dataclasses
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os

from database.entity import Word

dataList = Word.select()

def download_html(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print(f"Failed to get {url}")
    return None
  
def save_html(html, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

with ThreadPoolExecutor(max_workers=50) as executor:
    htmls = []
    for i, data in enumerate(dataList):
        url = data.definition_url
        print('downloading', url)
        continue
        html = executor.submit(download_html, url).result()
        if html is not None:
          filename = os.path.join('C:\\Users\\Kolar\\IdeaProjects\\oxford-word-list\\reader\\html_files', f'file{i}.html')
          save_html(html, filename)
        time.sleep(1)  # add delay between requests