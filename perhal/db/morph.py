import requests
import json
import os

# Langkah 1: Mengambil data dari URL
url = "https://static.quranwbw.com/data/v4/meta/verseKeyData.json"
response = requests.get(url)
data = response.json()

# Langkah 2: Menyimpan data ke dalam file lokal
with open("verseKeyData.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Langkah 3: Iterasi pada setiap key dalam data
for verse_key, verse_data in data.items():
    surat, ayat = verse_key.split(":")
    words = verse_data["words"]

    # Langkah 5: Iterasi dari 1 hingga words + 1
    for iterasi in range(1, words + 1):
        # Langkah 6: Mengambil data morphology dari URL
        morphology_url = f"https://api.quranwbw.com/v1/morphology?words={surat}:{ayat}:{iterasi}&word_translation=1&version=133&bypass_cache=false"
        morphology_response = requests.get(morphology_url)
        morphology_data = morphology_response.json()

        # Langkah 7: Menyimpan data morphology ke dalam file
        morph_dir = "morph"
        if not os.path.exists(morph_dir):
            os.makedirs(morph_dir)

        file_name = f"{morph_dir}/{surat}_{ayat}_{iterasi}.json"
        with open(file_name, "w", encoding="utf-8") as morph_file:
            json.dump(morphology_data, morph_file, ensure_ascii=False, indent=4)

        print(f"Data morphology untuk {verse_key}:{iterasi} telah disimpan di {file_name}")

print("Proses selesai.")
