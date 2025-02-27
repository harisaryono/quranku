import requests

def translate_text(text, source_lang='ar', target_lang='id'):
    url = "https://libretranslate.com/translate"
    payload = {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['translatedText']
    else:
        return f"Error: {response.status_code}"

# Contoh penggunaan
arabic_text = "مرحبا كيف حالك"
translated_text = translate_text(arabic_text, source_lang='ar', target_lang='id')
print(f"Teks asli: {arabic_text}")
print(f"Terjemahan: {translated_text}")
