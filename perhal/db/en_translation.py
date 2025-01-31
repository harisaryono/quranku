import json
import requests

# Fungsi untuk memproses setiap surah
def process_surah(surah):
    filename = f"{surah}.json"
    
    # Baca data dari file lokal
    try:
        with open(filename, "r", encoding="utf-8") as file:
            var1 = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan.")
        return
    
    # Ambil data dari API
    url = f"https://api.quranwbw.com/v1/chapter?chapter={surah}&word_type=1&word_translation=1&verse_translation=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Gagal mengambil data dari API untuk surah {surah}")
        return
    
    var2 = response.json()
    
    # Proses perubahan struktur JSON
    for verse, details in var1["data"]["verses"].items():
        details["words"]["id"] = details["words"].pop("translation")  # Ubah translation -> id
        details["words"]["ar"] = details["words"].pop("arabic")        # Ubah arabic -> ar
        
        # Tambahkan words.en dari var2
        if verse in var2["data"]["verses"]:
            details["words"]["en"] = var2["data"]["verses"][verse]["words"]["translation"]
    
    # Simpan kembali file JSON
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(var1, file, ensure_ascii=False, indent=4)
    print(f"Berhasil memperbarui {filename}")

# Proses untuk surah 1 hingga 14
for surah in range(2, 115):
    process_surah(surah)
