import json

# Membaca data dari file JSON
with open("verseKeyData.json", "r", encoding="utf-8") as file:
    verse_key_data = json.load(file)

with open("quran_data.json", "r", encoding="utf-8") as file:
    quran_data = json.load(file)

# Menyimpan hasil kesalahan
wrong_pages = []

# Iterasi pada data quran_data
for halaman, surah_data in quran_data.items():
    for surat_ayat, ayat_data in surah_data.items():
        surat, ayat = surat_ayat.split("_")
        verse_key = f"{surat}:{ayat}"
        
        # Cek apakah verse_key ada dalam verseKeyData
        if verse_key in verse_key_data:
            correct_page = verse_key_data[verse_key]["page"]
            print(surat_ayat,halaman,correct_page)
            if int(halaman) != correct_page:
                wrong_pages.append({
                    "surat_ayat": surat_ayat,
                    "halaman_salah": halaman,
                    "halaman_seharusnya": correct_page
                })

# Menampilkan hasil kesalahan
if wrong_pages:
    print("Kesalahan penomoran halaman ditemukan:")
    for entry in wrong_pages:
        print(f"{entry['surat_ayat']}: halaman {entry['halaman_salah']} seharusnya {entry['halaman_seharusnya']}")
else:
    print("Tidak ada kesalahan penomoran halaman.")

