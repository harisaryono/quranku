import json
import requests

# Baca data dari quran_data.json
json_file_path = 'quran_data.json'
with open(json_file_path, 'r', encoding='utf-8') as file:
    quran_data = json.load(file)

# Fungsi untuk mengambil data dari URL
def fetch_translation(surat_number):
    url = f"https://static.quranwbw.com/data/v3/{surat_number}/word-translations/arabic.json?v1732752118"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Proses untuk semua surat (1-114)
for surat in range(1, 115):
    translation_data = fetch_translation(surat)

    for page, page_data in quran_data.items():
        for verse_key, verse_data in page_data.items():
            surah_number, ayah_number = map(int, verse_key.split('_'))
            
            # Jika nomor surat sesuai dengan surat yang sedang diproses
            if surah_number == surat:
                if str(ayah_number) in translation_data:
                    words_list = translation_data[str(ayah_number)]['w'].split('|')
                    for i, word_data in enumerate(verse_data["words"]):
                        if i < len(words_list):
                            arabic_text = words_list[i].split('/')[0]  # Ambil teks Arab pertama
                            word_data['ar'] = arabic_text  # Update teks Arab
                            print(f'data awal {word_data["ar"]} diubah {arabic_text}')

# Simpan kembali data ke quran_data.json
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(quran_data, file, ensure_ascii=False, indent=4)

print("Update selesai. quran_data.json telah diperbarui.")

