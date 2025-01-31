import requests

# URL API
url = "https://api.quranwbw.com/v1/chapter?chapter=1&word_type=3&word_translation=1&verse_translation=1"

# Mengambil data dari API
response = requests.get(url)
data = response.json()

# Memproses data
verses = data["data"]["verses"]
for verse, details in verses.items():
    arabic_words = details["words"]["arabic"].split("||")
    translation_words = details["words"]["translation"].split("||")
    
    for i, (ar, en) in enumerate(zip(arabic_words, translation_words), start=1):
        print(f"{verse}:{i} {ar}, {en}")
