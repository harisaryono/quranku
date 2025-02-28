import json

# Langkah 1: Muat data dari verseKeyData.json
with open("verseKeyData.json", "r", encoding="utf-8") as file:
    verse_data = json.load(file)

# Langkah 2: Muat data dari quran_data.json
with open("quran_data.json", "r", encoding="utf-8") as file:
    quran_data = json.load(file)

# Langkah 3: Bandingkan halaman dari kedua file dalam range 120-130
print("Perbandingan halaman dalam range 120-130:")
for page, surat_ayat_data in quran_data.items():
    # Filter halaman dalam range 120-130
    if 120 <= int(page) <= 130:
        for surat_ayat, details in surat_ayat_data.items():
            # Ekstrak surat dan ayat dari format surat_ayat (misal: "1_1")
            surat, ayat = surat_ayat.split("_")
            verse_key = f"{surat}:{ayat}"  # Format key di verseKeyData.json

            # Dapatkan halaman yang benar dari verseKeyData.json
            if verse_key in verse_data:
                correct_page = verse_data[verse_key]["page"]
                current_page = int(page)  # Halaman di quran_data.json

                # Bandingkan halaman
                if current_page == correct_page:
                    status = "Sesuai"
                else:
                    status = "Tidak Sesuai"

                # Cetak hasil perbandingan
                print(f"{surat_ayat}: Halaman saat ini = {current_page}, Halaman yang benar = {correct_page} -> {status}")
            else:
                print(f"{surat_ayat}: Key {verse_key} tidak ditemukan di verseKeyData.json")
