import requests
import json

# Loop untuk semua chapter dari 1 sampai 114
for chapter in range(1, 115):
    url = f"https://api.quranwbw.com/v1/chapter?chapter={chapter}&word_type=1&word_translation=4&verse_translation=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        filename = f"{chapter}.json"
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print(f"Saved: {filename}")
    else:
        print(f"Failed to fetch chapter {chapter}, Status Code: {response.status_code}")
