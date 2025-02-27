import requests

# URL API LibreTranslate yang berjalan di Docker
url = 'http://localhost:5000/translate'

# Teks yang akan diterjemahkan
text = 'Hello, how are you?'

# Mengatur parameter untuk permintaan
params = {
    'q': text,              # Teks yang akan diterjemahkan
    'source': 'en',         # Bahasa sumber
    'target': 'id'          # Bahasa target
}

# Mengirimkan permintaan POST ke API
response = requests.post(url, data=params)

# Mengecek hasil terjemahan
if response.status_code == 200:
    translated_text = response.json()['translatedText']
    print(f"Translated Text: {translated_text}")
else:
    print("Error:", response.status_code)

