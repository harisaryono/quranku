import sqlite3
import json

def save_data_to_json(db_path, json_file_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Set row factory to allow access by column name
    cursor = conn.cursor()

    # Query untuk mengambil data dari tabel data dan qkata
    cursor.execute("""
        SELECT d.kode, d.hal, d.juz, d.nama_surat, d.nomor_surat, d.nomor_ayat, d.tashkeel, q.nomorkata, q.ar, q.id,q.en
        FROM data d
        JOIN qkata q ON d.kode = q.kode
        ORDER BY d.nomor_surat, d.nomor_ayat, q.nomorkata
    """)

    # Ambil hasil query
    rows = cursor.fetchall()
    conn.close()

    # Siapkan struktur data
    data = {}

    # Menyusun data berdasarkan halaman
    for row in rows:
        # Menggunakan row sebagai dictionary berdasarkan nama kolom
        page_number = row['hal']
        surah_number = row['nomor_surat']
        ayah_number = row['nomor_ayat']
        surah_name = row['nama_surat']
        tashkeel = row['tashkeel']
        juz = row['juz']
        word_ar = row['ar']  # Kata dari qkata
        word_id = row['id']  # ID kata
        word_en = row['en'] # kata dalam bahasa inggris

        # Format kunci untuk ayat
        verse_key = f"{surah_number}_{ayah_number}"

        # Jika halaman belum ada dalam data, buat halaman baru
        if page_number not in data:
            data[page_number] = {}

        # Jika ayat belum ada, buat entri untuk ayat tersebut
        if verse_key not in data[page_number]:
            data[page_number][verse_key] = {
                'nama_surat': surah_name,
                'tashkeel': tashkeel,
                'juz': juz,
                'words': []  # List kata-kata untuk ayat ini
            }

        # Menambahkan kata ke dalam daftar kata untuk ayat ini
        data[page_number][verse_key]['words'].append({'ar': word_ar, 'id': word_id,'en':word_en})

    # Menyimpan data ke file JSON
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Panggil fungsi untuk menyimpan data
db_path = '/home/harry/Documents/pCloudSync/database/quran/alquran2.db'
json_file_path = '/home/harry/GIT/quranku/perhal/quran_data.json'
save_data_to_json(db_path, json_file_path)

