from database.entity import Word

# python3 -m export.csv-exporter
for word in Word.select():
  print(word.word, word.definitions)